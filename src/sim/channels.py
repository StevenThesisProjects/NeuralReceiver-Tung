"""Channel modeling module for nrx-bounded simulation pipeline.

Provides 3GPP TR 38.901 Clustered Delay Line (CDL) channel generation
with deterministic seeding and parameterization via config/config.yaml.
"""

from __future__ import annotations

import math
from typing import Any, Dict, Optional, Tuple, Union

import numpy as np
import torch

from src.config import load_config

try:
    import sionna
    import sionna.phy
    import sionna.phy.channel.tr38901 as tr
    from sionna.phy.object import Object
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
    _SIONNA_AVAILABLE = False


class SyntheticCDL(torch.nn.Module):
    """Fallback synthetic CDL channel model when Sionna is unavailable or on CPU test environments.

    Emulates the tensor structure and statistical impulse response of a 3GPP CDL channel.
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
        device: Optional[Union[str, torch.device]] = None,
    ):
        super().__init__()
        self.model = model
        self.delay_spread = float(delay_spread)
        self.carrier_frequency = float(carrier_frequency)
        self.num_rx_ant = int(num_rx_ant)
        self.num_tx_ant = int(num_tx_ant)
        self.speed = float(speed)
        self.seed = int(seed)
        self.device = str(device) if device is not None else "cpu"
        self._generator = torch.Generator(device=self.device)
        self._generator.manual_seed(self.seed)
        self.num_paths = 24

    def reset_seed(self, seed: Optional[int] = None) -> None:
        """Reset the internal generator seed."""
        if seed is not None:
            self.seed = seed
        self._generator.manual_seed(self.seed)

    def __call__(
        self,
        batch_size: int,
        num_time_steps: int,
        sampling_frequency: float,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """Generate synthetic CDL channel impulse response matching Sionna CDL tensor shape."""
        # delays: [batch, num_rx, num_tx, num_paths]
        # Exponential delay distribution scaled by delay_spread
        delays_base = torch.linspace(0.0, self.delay_spread * 3.0, self.num_paths, device=self.device)
        delays = delays_base.view(1, 1, 1, self.num_paths).expand(batch_size, 1, self.num_tx_ant, self.num_paths).clone()

        # Complex path gains with Rayleigh fading and exponential power profile
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
) -> Any:
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
        Maximum UE speed [m/s]. Defaults to cfg['channel']['speed_1'].
    cfg : dict, optional
        Pre-loaded configuration dictionary. Loaded automatically if None.
    use_synthetic : bool, optional
        Force synthetic channel generator fallback.
    device : str or torch.device, optional
        Target computation device ('cpu', 'cuda'). Defaults to config device.

    Returns
    -------
    CDL or SyntheticCDL
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
        speed_max = float(chan_cfg.get("speed_1", chan_cfg.get("speed_max", v)))
    else:
        speed_max = float(speed_max)

    if delay_spread is None:
        raw_ds = chan_cfg.get("delay_spread", 100e-9)
        if isinstance(raw_ds, dict):
            # Fallback for legacy dict if encountered
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

    if device is None:
        preferred_device = train_cfg.get("device", "cuda")
        device = preferred_device if torch.cuda.is_available() and "cuda" in str(preferred_device).lower() else "cpu"

    # Fallback to synthetic if Sionna unavailable or explicitly requested
    if not _SIONNA_AVAILABLE or use_synthetic:
        return SyntheticCDL(
            model=model,
            delay_spread=delay_spread,
            carrier_frequency=carrier_frequency,
            num_rx_ant=rx_ant,
            num_tx_ant=tx_ant,
            speed=v,
            seed=seed,
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
    cdl = tr.CDL(
        model=model,
        delay_spread=delay_spread,
        carrier_frequency=carrier_frequency,
        ut_array=ut_array,
        bs_array=bs_array,
        direction=direction,
        min_speed=v,
        max_speed=speed_max,
        device=device,
    )

    # Bind deterministic per-instance generator
    dev_str = str(device) if device is not None else str(cdl.device)
    gen = torch.Generator(device=dev_str)
    gen.manual_seed(seed)
    cdl._generator = gen
    if hasattr(cdl, "_cir_gen"):
        cdl._cir_gen._generator = gen
    cdl.seed = seed

    return cdl
