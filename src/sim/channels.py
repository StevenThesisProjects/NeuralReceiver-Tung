"""Channel modeling module for nrx-bounded simulation pipeline.

Provides 3GPP TR 38.901 Clustered Delay Line (CDL) channel generation
with deterministic seeding and parameterization via config/config.yaml:
- SionnaCDLChannel: Subclass of Sionna TR 38.901 CDL channel with deterministic
  seeding, per-instance RNG, and sample() method for frequency-domain CSI tensors.
- SyntheticCDLChannel: Robust pure-PyTorch fallback channel when Sionna is absent.
- make_cdl: Factory creating channel instance from single-source configuration.
"""

from __future__ import annotations

import math
from typing import Any, Dict, Optional, Tuple, Union

import numpy as np
import torch

from src.config import load_config
from src.utils import set_all_seeds

try:
    import sionna
    import sionna.phy
    import sionna.phy.channel.tr38901 as tr
    from sionna.phy.channel import OFDMChannel
    from sionna.phy.object import Object
    from sionna.phy.ofdm import ResourceGrid
    from sionna.phy import config as sionna_config
    _SIONNA_AVAILABLE = True

    # Patch Object.torch_rng to support per-instance generator determinism
    _orig_torch_rng = Object.torch_rng.fget

    def _custom_torch_rng(self):
        if hasattr(self, "_generator") and self._generator is not None:
            return self._generator
        return _orig_torch_rng(self)

    Object.torch_rng = property(_custom_torch_rng)

except ImportError:
    try:
        import sionna
        import sionna.channel.tr38901 as tr  # type: ignore
        from sionna.channel import OFDMChannel  # type: ignore
        from sionna.ofdm import ResourceGrid  # type: ignore
        _SIONNA_AVAILABLE = True
    except ImportError:
        _SIONNA_AVAILABLE = False
        tr = None  # type: ignore


class SyntheticCDLChannel(torch.nn.Module):
    """Fallback synthetic CDL channel model when Sionna is unavailable or on CPU test environments.

    Emulates the tensor structure and statistical impulse response of a 3GPP CDL channel.
    Supports both CIR output (a, tau) and frequency response sampling sample(batch_size).
    """

    def __init__(
        self,
        model: str = "C",
        delay_spread: float = 100e-9,
        carrier_frequency: float = 3.5e9,
        num_rx_ant: int = 2,
        num_tx_ant: int = 1,
        speed: float = 0.0,
        seed: int = 42,
        num_ofdm_symbols: int = 14,
        fft_size: int = 128,
        subcarrier_spacing: float = 30000.0,
        device: Optional[Union[str, torch.device]] = None,
    ) -> None:
        super().__init__()
        self.model = str(model)
        self.delay_spread = float(delay_spread)
        self.carrier_frequency = float(carrier_frequency)
        self.rx_ant = int(num_rx_ant)
        self.tx_ant = int(num_tx_ant)
        self.num_rx_ant = self.rx_ant
        self.num_tx_ant = self.tx_ant
        self.speed = float(speed)
        self.v = self.speed
        self._min_speed = float(speed)
        self._max_speed = float(speed)
        self.seed = int(seed) if seed is not None else 42
        self._current_seed = self.seed
        self.num_ofdm_symbols = int(num_ofdm_symbols)
        self.fft_size = int(fft_size)
        self.subcarrier_spacing = float(subcarrier_spacing)
        self.device = str(device) if device is not None else "cpu"
        self._generator = torch.Generator(device=self.device)
        self._generator.manual_seed(self.seed)
        self.num_paths = 24

    def reset_seed(self, seed: Optional[int] = None) -> None:
        """Reset the internal generator seed."""
        if seed is not None:
            self.seed = seed
            self._current_seed = seed
        self._generator.manual_seed(self.seed)

    def sample(
        self,
        batch_size: int = 16,
        num_ofdm_symbols: Optional[int] = None,
        fft_size: Optional[int] = None,
    ) -> torch.Tensor:
        """Generate channel frequency response tensor.

        Returns
        -------
        torch.Tensor
            Complex tensor of shape (batch_size, num_rx_ant, num_tx_ant, num_ofdm_symbols, fft_size).
        """
        num_sym = num_ofdm_symbols if num_ofdm_symbols is not None else self.num_ofdm_symbols
        n_fft = fft_size if fft_size is not None else self.fft_size

        gen = torch.Generator(device=self.device).manual_seed(self._current_seed)
        self._current_seed = (self._current_seed + 1) & 0x7FFFFFFF

        # 24 multipath clusters
        delays_base = torch.linspace(0.0, self.delay_spread * 3.0, self.num_paths, device=self.device)
        pwr = torch.exp(-delays_base / (self.delay_spread + 1e-12))
        pwr = pwr / torch.sum(pwr)

        real = torch.randn(
            (batch_size, self.rx_ant, self.tx_ant, self.num_paths),
            generator=gen,
            device=self.device,
        )
        imag = torch.randn(
            (batch_size, self.rx_ant, self.tx_ant, self.num_paths),
            generator=gen,
            device=self.device,
        )
        taps = torch.complex(real, imag) * torch.sqrt(pwr.view(1, 1, 1, -1) / 2.0)

        # Subcarrier frequencies
        k_indices = torch.arange(n_fft, dtype=torch.float32, device=self.device) - (n_fft / 2.0)
        freqs = k_indices * self.subcarrier_spacing
        phases = 2.0 * math.pi * torch.outer(freqs, delays_base)
        steering = torch.exp(torch.complex(torch.zeros_like(phases), -phases))

        # Doppler time variation
        c = 3.0e8
        max_doppler = (self.v * self.carrier_frequency) / c
        sym_duration = 1.0 / self.subcarrier_spacing
        t_indices = torch.arange(num_sym, dtype=torch.float32, device=self.device) * sym_duration
        doppler_phases = 2.0 * math.pi * max_doppler * t_indices
        doppler_rot = torch.exp(torch.complex(torch.zeros_like(doppler_phases), doppler_phases))

        h_freq = torch.matmul(taps, steering.t())  # (batch, rx_ant, tx_ant, n_fft)
        H = h_freq.unsqueeze(3) * doppler_rot.view(1, 1, 1, num_sym, 1)

        energy = torch.mean(torch.abs(H) ** 2)
        if energy > 0:
            H = H / torch.sqrt(energy)

        return H

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Dual-purpose callable supporting both CIR generation and frequency tensor sampling.

        If called with 1 positional int argument (batch_size): returns frequency tensor H.
        If called with (batch_size, num_time_steps, sampling_frequency): returns CIR (h, delays).
        """
        if len(args) == 1 and isinstance(args[0], int) and not kwargs:
            return self.sample(batch_size=args[0])
        if "batch_size" in kwargs and len(args) == 0 and "num_time_steps" not in kwargs:
            return self.sample(**kwargs)

        # Standard CIR signature: (batch_size, num_time_steps, sampling_frequency)
        batch_size = args[0] if len(args) > 0 else kwargs.get("batch_size", 1)
        num_time_steps = args[1] if len(args) > 1 else kwargs.get("num_time_steps", self.num_ofdm_symbols)
        sampling_frequency = args[2] if len(args) > 2 else kwargs.get("sampling_frequency", self.fft_size * self.subcarrier_spacing)

        delays_base = torch.linspace(0.0, self.delay_spread * 3.0, self.num_paths, device=self.device)
        delays = delays_base.view(1, 1, 1, self.num_paths).expand(batch_size, 1, self.num_tx_ant, self.num_paths).clone()

        power_profile = torch.exp(-delays_base / (self.delay_spread + 1e-12)).view(1, 1, 1, 1, 1, self.num_paths, 1)
        power_profile = power_profile / torch.sum(power_profile)

        real_part = torch.randn(
            (batch_size, 1, self.num_rx_ant, self.num_tx_ant, 1, self.num_paths, num_time_steps),
            generator=self._generator,
            device=self.device,
        )
        imag_part = torch.randn(
            (batch_size, 1, self.num_rx_ant, self.num_tx_ant, 1, self.num_paths, num_time_steps),
            generator=self._generator,
            device=self.device,
        )
        h = torch.complex(real_part, imag_part) * torch.sqrt(power_profile / 2.0)

        return h, delays


# Alias for backward compatibility
SyntheticCDL = SyntheticCDLChannel


if _SIONNA_AVAILABLE:
    class SionnaCDLChannel(tr.CDL):
        """Sionna 3GPP TR 38.901 CDL Channel subclass with deterministic tensor sampling."""

        def __init__(
            self,
            model: str,
            delay_spread: float,
            carrier_frequency: float,
            ut_array: Any,
            bs_array: Any,
            direction: str = "uplink",
            min_speed: float = 0.0,
            max_speed: float = 0.0,
            seed: int = 42,
            rx_ant: int = 2,
            tx_ant: int = 1,
            num_ofdm_symbols: int = 14,
            fft_size: int = 128,
            subcarrier_spacing: float = 30000.0,
            resource_grid: Any = None,
            **kwargs: Any,
        ) -> None:
            super().__init__(
                model=model,
                delay_spread=delay_spread,
                carrier_frequency=carrier_frequency,
                ut_array=ut_array,
                bs_array=bs_array,
                direction=direction,
                min_speed=min_speed,
                max_speed=max_speed,
                **kwargs,
            )
            self.seed = int(seed) if seed is not None else 42
            self._current_seed = self.seed
            self.rx_ant = int(rx_ant)
            self.tx_ant = int(tx_ant)
            self.num_rx_ant = self.rx_ant
            self.num_tx_ant = self.tx_ant
            self.num_ofdm_symbols = int(num_ofdm_symbols)
            self.fft_size = int(fft_size)
            self.subcarrier_spacing = float(subcarrier_spacing)
            self._rg = resource_grid
            self._ofdm_ch = None

        def _get_ofdm_channel(
            self,
            num_ofdm_symbols: Optional[int] = None,
            fft_size: Optional[int] = None,
        ) -> OFDMChannel:
            num_sym = num_ofdm_symbols if num_ofdm_symbols is not None else self.num_ofdm_symbols
            n_fft = fft_size if fft_size is not None else self.fft_size

            if self._ofdm_ch is None or self._rg.num_ofdm_symbols != num_sym or self._rg.fft_size != n_fft:
                cfg = load_config()
                phy = cfg.get("phy", {})
                self._rg = ResourceGrid(
                    num_ofdm_symbols=num_sym,
                    fft_size=n_fft,
                    subcarrier_spacing=self.subcarrier_spacing,
                    num_tx=self.tx_ant,
                    num_streams_per_tx=1,
                    cyclic_prefix_length=phy.get("cyclic_prefix_length", 0),
                    dc_null=phy.get("dc_null", True),
                    pilot_pattern=phy.get("pilot_pattern", "kronecker"),
                    pilot_ofdm_symbol_indices=phy.get("pilot_ofdm_symbol_indices", [2, 11]),
                    num_guard_carriers=phy.get("num_guard_carriers", [5, 6]),
                )
                self._ofdm_ch = OFDMChannel(self, self._rg, normalize_channel=True, return_channel=True)
            return self._ofdm_ch

        def sample(
            self,
            batch_size: int = 16,
            num_ofdm_symbols: Optional[int] = None,
            fft_size: Optional[int] = None,
        ) -> torch.Tensor:
            """Sample channel frequency response tensor.

            Returns
            -------
            torch.Tensor
                Complex channel tensor of shape:
                (batch_size, rx_ant, tx_ant, num_ofdm_symbols, fft_size)
            """
            if self._current_seed is not None:
                set_all_seeds(self._current_seed)
                sionna_config.seed = self._current_seed
                self._current_seed = (self._current_seed + 1) & 0x7FFFFFFF

            ofdm_ch = self._get_ofdm_channel(num_ofdm_symbols, fft_size)
            h = ofdm_ch.generate(batch_size)
            # sionna returns (batch_size, num_rx, num_rx_ant, num_tx, num_tx_ant, num_ofdm_symbols, fft_size)
            if h.dim() == 7:
                h = h[:, 0, :, 0, :, :, :]
            return h

        def __call__(self, *args: Any, **kwargs: Any) -> Any:
            """Dual-purpose callable supporting both CIR generation and frequency tensor sampling.

            If called with 1 positional int argument (batch_size): returns frequency tensor H.
            If called with (batch_size, num_time_steps, sampling_frequency): calls Sionna CDL forward.
            """
            if len(args) == 1 and isinstance(args[0], int) and not kwargs:
                return self.sample(batch_size=args[0])
            if "batch_size" in kwargs and len(args) == 0 and "num_time_steps" not in kwargs:
                return self.sample(**kwargs)
            return super().__call__(*args, **kwargs)


def make_cdl(
    model: Optional[str] = None,
    v: Optional[float] = None,
    delay_spread: Optional[float] = None,
    seed: Optional[int] = None,
    carrier_frequency: Optional[float] = None,
    rx_ant: Optional[int] = None,
    tx_ant: Optional[int] = None,
    direction: str = "uplink",
    speed_max: Optional[float] = None,
    cfg: Optional[Dict[str, Any]] = None,
    use_synthetic: bool = False,
    device: Optional[Union[str, torch.device]] = None,
    **kwargs: Any,
) -> Union[SionnaCDLChannel, SyntheticCDLChannel]:
    """Create a Sionna 3GPP CDL channel model instance with deterministic seeding.

    Parameters
    ----------
    model : str, optional
        CDL profile ('A', 'B', 'C', 'D'). Defaults to cfg['channel']['cdl_model'].
    v : float, optional
        Minimum UE speed [m/s]. Defaults to cfg['channel']['speed'].
    delay_spread : float, optional
        RMS delay spread [s]. Defaults to cfg['channel']['delay_spread'].
    seed : int, optional
        Deterministic random seed. Defaults to cfg['seed'].
    carrier_frequency : float, optional
        Carrier frequency [Hz]. Defaults to cfg['phy']['carrier_frequency'].
    rx_ant : int, optional
        Number of receive antenna elements. Defaults to cfg['phy']['num_rx_antennas'].
    tx_ant : int, optional
        Number of transmit antenna elements. Defaults to cfg['phy']['num_tx_antennas'].
    direction : str, optional
        Link direction ('uplink' or 'downlink'). Default is 'uplink'.
    speed_max : float, optional
        Maximum UE speed [m/s]. Defaults to v if None.
    cfg : dict, optional
        Pre-loaded configuration dictionary. Loaded automatically if None.
    use_synthetic : bool, optional
        Force synthetic channel generator fallback.
    device : str or torch.device, optional
        Target computation device ('cpu', 'cuda'). Defaults to config device.

    Returns
    -------
    SionnaCDLChannel or SyntheticCDLChannel
        Configured and seeded CDL channel model instance.
    """
    if cfg is None:
        cfg = load_config()

    # Extract default configuration values
    phy_cfg = cfg.get("phy", {})
    chan_cfg = cfg.get("channel", {})
    train_cfg = cfg.get("training", {})

    if model is None:
        raw_model = chan_cfg.get("cdl_model", "C")
        # Strip "CDL-" prefix if present
        model = raw_model[-1] if raw_model.upper().startswith("CDL-") else raw_model

    if v is None:
        v = float(chan_cfg.get("speed", chan_cfg.get("speed_min", 0.0)))
    else:
        v = float(v)

    if speed_max is None:
        speed_max = float(v)
    else:
        speed_max = float(speed_max)

    if delay_spread is None:
        raw_ds = chan_cfg.get("delay_spread", 100e-9)
        if isinstance(raw_ds, dict):
            delay_spread = float(raw_ds.get("cdl_c", 100e-9))
        else:
            delay_spread = float(raw_ds)
    else:
        delay_spread = float(delay_spread)

    if seed is None:
        seed = int(cfg.get("seed", 42))
    else:
        seed = int(seed)

    if carrier_frequency is None:
        carrier_frequency = float(phy_cfg.get("carrier_frequency", 3.5e9))
    else:
        carrier_frequency = float(carrier_frequency)

    if rx_ant is None:
        rx_ant = int(phy_cfg.get("num_rx_antennas", phy_cfg.get("num_rx_ant", 2)))
    else:
        rx_ant = int(rx_ant)

    if tx_ant is None:
        tx_ant = int(phy_cfg.get("num_tx_antennas", phy_cfg.get("num_tx_ant", 1)))
    else:
        tx_ant = int(tx_ant)

    num_ofdm_symbols = int(phy_cfg.get("num_ofdm_symbols", 14))
    fft_size = int(phy_cfg.get("fft_size", 128))
    subcarrier_spacing = float(phy_cfg.get("subcarrier_spacing", 30000.0))

    if device is None:
        preferred_device = train_cfg.get("device", "cuda")
        device = preferred_device if torch.cuda.is_available() and "cuda" in str(preferred_device).lower() else "cpu"

    # Fallback to synthetic if Sionna unavailable or explicitly requested
    if not _SIONNA_AVAILABLE or use_synthetic:
        return SyntheticCDLChannel(
            model=model,
            delay_spread=delay_spread,
            carrier_frequency=carrier_frequency,
            num_rx_ant=rx_ant,
            num_tx_ant=tx_ant,
            speed=v,
            seed=seed,
            num_ofdm_symbols=num_ofdm_symbols,
            fft_size=fft_size,
            subcarrier_spacing=subcarrier_spacing,
            device=device,
        )

    # Initialize Sionna determinism
    sionna_config.seed = seed
    torch.manual_seed(seed)
    np.random.seed(seed)

    # Configure Transmitter Array (single antenna element for SIMO/SISO)
    if tx_ant == 1:
        ut_array = tr.Antenna(
            polarization="single",
            polarization_type="V",
            antenna_pattern="38.901",
            carrier_frequency=carrier_frequency,
            device=device,
        )
    else:
        num_cols = max(1, tx_ant // 2)
        ut_array = tr.AntennaArray(
            num_rows=1,
            num_cols=num_cols,
            polarization="dual" if tx_ant >= 2 else "single",
            polarization_type="VH" if tx_ant >= 2 else "V",
            antenna_pattern="38.901",
            carrier_frequency=carrier_frequency,
            device=device,
        )

    # Configure Receiver Array (dual-polarized for SIMO 1x2)
    if rx_ant == 2:
        bs_array = tr.AntennaArray(
            num_rows=1,
            num_cols=1,
            polarization="dual",
            polarization_type="VH",
            antenna_pattern="38.901",
            carrier_frequency=carrier_frequency,
            device=device,
        )
    elif rx_ant == 1:
        bs_array = tr.Antenna(
            polarization="single",
            polarization_type="V",
            antenna_pattern="38.901",
            carrier_frequency=carrier_frequency,
            device=device,
        )
    else:
        num_cols = max(1, rx_ant // 2)
        bs_array = tr.AntennaArray(
            num_rows=1,
            num_cols=num_cols,
            polarization="dual",
            polarization_type="VH",
            antenna_pattern="38.901",
            carrier_frequency=carrier_frequency,
            device=device,
        )

    # Instantiate Sionna CDL model
    cdl = SionnaCDLChannel(
        model=model,
        delay_spread=delay_spread,
        carrier_frequency=carrier_frequency,
        ut_array=ut_array,
        bs_array=bs_array,
        direction=direction,
        min_speed=v,
        max_speed=speed_max,
        seed=seed,
        rx_ant=rx_ant,
        tx_ant=tx_ant,
        num_ofdm_symbols=num_ofdm_symbols,
        fft_size=fft_size,
        subcarrier_spacing=subcarrier_spacing,
        device=device,
        **kwargs,
    )

    # Bind deterministic per-instance generator
    dev_str = str(device) if device is not None else str(cdl.device)
    gen = torch.Generator(device=dev_str)
    gen.manual_seed(seed)
    cdl._generator = gen
    if hasattr(cdl, "_cir_gen"):
        cdl._cir_gen._generator = gen

    return cdl
