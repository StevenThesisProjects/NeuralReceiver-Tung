"""Classical baseline receiver modules for SIMO OFDM links.

Provides baseline implementations:
- demap_lmmse: Single-tap SIMO LMMSE soft equalization and soft LLR demapping.
- b0_receiver: Baseline B0 with Least-Squares (LS) channel estimation (nearest-neighbor
  interpolation by default) and LMMSE demapper.
- b1_receiver: Baseline B1 with Perfect CSI (Genie-aided) and LMMSE demapper.

Supports Sionna components when available and pure PyTorch fallbacks when Sionna is absent.
"""

from __future__ import annotations

import math
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
import torch

from src.config import load_config
from src.sim.link import LinkConfig

try:
    import sionna
    import sionna.phy
    from sionna.phy.mapping import Constellation, Demapper
    from sionna.phy.mimo import StreamManagement
    from sionna.phy.ofdm import (
        LMMSEEqualizer,
        LSChannelEstimator,
        RemoveNulledSubcarriers,
        ResourceGrid,
    )
    from sionna.phy.utils import expand_to_rank

    _SIONNA_AVAILABLE = True
except ImportError:
    try:
        import sionna
        from sionna.mapping import Constellation, Demapper  # type: ignore
        from sionna.mimo import StreamManagement  # type: ignore
        from sionna.ofdm import (  # type: ignore
            LMMSEEqualizer,
            LSChannelEstimator,
            RemoveNulledSubcarriers,
            ResourceGrid,
        )
        from sionna.utils import expand_to_rank  # type: ignore

        _SIONNA_AVAILABLE = True
    except ImportError:
        _SIONNA_AVAILABLE = False


def _get_or_create_resource_grid(
    link_config: LinkConfig,
    device: Optional[Union[str, torch.device]] = None,
    pilot_seed: Optional[int] = None,
) -> Any:
    """Create deterministic Sionna ResourceGrid or synthetic equivalent."""
    effective_seed = pilot_seed if pilot_seed is not None else getattr(link_config, "seed", 42)
    try:
        import sionna
        if hasattr(sionna, "phy") and hasattr(sionna.phy, "config"):
            sionna.phy.config.seed = int(effective_seed)
        elif hasattr(sionna, "config"):
            sionna.config.seed = int(effective_seed)
    except Exception:
        pass
    return link_config.create_resource_grid(device=device)


# ==============================================================================
# Pure PyTorch Demapper Fallback Utilities
# ==============================================================================


def _pam_gray(b: np.ndarray) -> int:
    """Map binary vector to Gray-coded PAM constellation point."""
    if len(b) > 1:
        return (1 - 2 * b[0]) * (2 ** len(b[1:]) - _pam_gray(b[1:]))
    return 1 - 2 * b[0]


def _build_qam_constellation(num_bits_per_symbol: int) -> torch.Tensor:
    """Generate unit-power normalized Gray-coded QAM constellation points."""
    num_points = 2**num_bits_per_symbol
    pts = np.zeros([num_points], dtype=np.complex64)
    for i in range(num_points):
        b = np.array(list(np.binary_repr(i, num_bits_per_symbol)), dtype=np.int32)
        pts[i] = _pam_gray(b[0::2]) + 1j * _pam_gray(b[1::2])

    n = int(num_bits_per_symbol / 2)
    qam_var = 1.0 / (2 ** (n - 2)) * np.sum(np.linspace(1, 2**n - 1, 2 ** (n - 1), dtype=np.float32) ** 2)
    pts /= np.sqrt(qam_var)
    return torch.from_numpy(pts)


_CONSTELLATION_CACHE: Dict[int, Tuple[torch.Tensor, torch.Tensor, torch.Tensor]] = {}


def _get_qam_cache(num_bits_per_symbol: int, device: torch.device) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """Retrieve or build cached QAM constellation points and bit masks."""
    if num_bits_per_symbol not in _CONSTELLATION_CACHE:
        pts = _build_qam_constellation(num_bits_per_symbol)
        num_points = 2**num_bits_per_symbol
        m1_list = []
        m0_list = []
        for k in range(num_bits_per_symbol):
            m1_k = [format(i, f"0{num_bits_per_symbol}b")[k] == "1" for i in range(num_points)]
            m1_list.append(torch.tensor(m1_k, dtype=torch.bool))
            m0_list.append(~torch.tensor(m1_k, dtype=torch.bool))
        m1 = torch.stack(m1_list)
        m0 = torch.stack(m0_list)
        _CONSTELLATION_CACHE[num_bits_per_symbol] = (pts, m1, m0)

    pts, m1, m0 = _CONSTELLATION_CACHE[num_bits_per_symbol]
    return pts.to(device), m1.to(device), m0.to(device)


def _pytorch_demap_app(
    y: torch.Tensor,
    no: Union[float, torch.Tensor],
    num_bits_per_symbol: int,
) -> torch.Tensor:
    """Exact APP soft LLR demapper in pure PyTorch."""
    pts, m1, m0 = _get_qam_cache(num_bits_per_symbol, y.device)
    orig_shape = y.shape

    if not isinstance(no, torch.Tensor):
        no_tensor = torch.tensor(float(no), dtype=torch.float32, device=y.device)
    else:
        no_tensor = no.to(device=y.device, dtype=torch.float32)

    no_bcast = torch.broadcast_to(no_tensor, orig_shape)
    y_flat = y.reshape(-1)
    no_flat = no_bcast.reshape(-1).clamp(min=1e-12)

    dist_sq = (y_flat[:, None] - pts[None, :]).abs().square()
    logits = -dist_sq / no_flat[:, None]

    llrs = []
    for k in range(num_bits_per_symbol):
        l1 = torch.logsumexp(logits[:, m1[k]], dim=-1)
        l0 = torch.logsumexp(logits[:, m0[k]], dim=-1)
        llrs.append(l1 - l0)

    llr_stacked = torch.stack(llrs, dim=-1)
    out_shape = list(orig_shape[:-1]) + [orig_shape[-1] * num_bits_per_symbol]
    return llr_stacked.reshape(out_shape)


def _get_active_subcarrier_indices(link_config: LinkConfig) -> List[int]:
    """Return indices of active subcarriers excluding guard bands and DC null."""
    guards = link_config.num_guard_carriers
    dc = link_config.fft_size // 2 if link_config.dc_null else -1
    return [
        i
        for i in range(link_config.fft_size)
        if i >= guards[0] and i < link_config.fft_size - guards[1] and i != dc
    ]


def _pytorch_ls_channel_estimator(
    y: torch.Tensor,
    link_config: LinkConfig,
    interpolation_type: str = "nn",
    no: Union[float, torch.Tensor] = 0.0,
    resource_grid: Optional[Any] = None,
    pilot_seed: Optional[int] = None,
) -> Tuple[torch.Tensor, torch.Tensor]:
    """Pure PyTorch fallback for LS channel estimation with nearest-neighbor interpolation."""
    y_4d = y.squeeze(1) if y.ndim == 5 else y  # [B, rx_ant, T, F]
    batch_size, rx_ant, num_symbols, fft_size = y_4d.shape

    active_sc = _get_active_subcarrier_indices(link_config)
    y_eff = y_4d[:, :, :, active_sc]  # [B, rx_ant, T, F_eff]
    pilot_indices = link_config.pilot_ofdm_symbol_indices  # e.g. [2, 11]

    rg = (
        resource_grid
        if resource_grid is not None
        else _get_or_create_resource_grid(link_config, device=y.device, pilot_seed=pilot_seed)
    )

    # Pilot symbols
    if hasattr(rg, "pilot_pattern") and hasattr(rg.pilot_pattern, "pilots"):
        pilots = rg.pilot_pattern.pilots.reshape(-1).to(y.device)
    else:
        pilots = torch.ones(len(active_sc) * len(pilot_indices), dtype=torch.complex64, device=y.device)

    num_sc_eff = len(active_sc)
    h_pilot_estimates = []
    for p_idx, sym_t in enumerate(pilot_indices):
        p_slice = pilots[p_idx * num_sc_eff : (p_idx + 1) * num_sc_eff]
        h_sym = y_eff[:, :, sym_t, :] / p_slice[None, None, :]
        h_pilot_estimates.append(h_sym)

    # Time interpolation
    h_hat_eff = torch.empty_like(y_eff)
    if interpolation_type == "lin" and len(pilot_indices) == 2:
        t0, t1 = pilot_indices[0], pilot_indices[1]
        h0, h1 = h_pilot_estimates[0], h_pilot_estimates[1]
        for t in range(num_symbols):
            if t <= t0:
                h_hat_eff[:, :, t, :] = h0
            elif t >= t1:
                h_hat_eff[:, :, t, :] = h1
            else:
                alpha = (t - t0) / (t1 - t0)
                h_hat_eff[:, :, t, :] = (1.0 - alpha) * h0 + alpha * h1
    else:
        # Default: Nearest-neighbor ('nn')
        for t in range(num_symbols):
            closest_p_idx = int(np.argmin([abs(t - p) for p in pilot_indices]))
            h_hat_eff[:, :, t, :] = h_pilot_estimates[closest_p_idx]

    # Format into 7D shape matching Sionna: [B, 1, rx_ant, 1, 1, T, F_eff]
    h_hat = h_hat_eff[:, None, :, None, None, :, :]
    err_var = torch.tensor(float(no) if not isinstance(no, torch.Tensor) else float(no.item()), device=y.device)
    return h_hat, err_var


# ==============================================================================
# Public API
# ==============================================================================


def demap_lmmse(
    y: torch.Tensor,
    h_hat: torch.Tensor,
    no: Union[float, torch.Tensor],
    num_bits_per_symbol: Optional[int] = None,
    link_config: Optional[LinkConfig] = None,
    err_var: Union[float, torch.Tensor] = 0.0,
    data_only: bool = True,
    resource_grid: Optional[Any] = None,
    pilot_seed: Optional[int] = None,
) -> torch.Tensor:
    """Compute single-tap SIMO LMMSE soft equalization and soft LLR demapping.

    Single-tap SIMO Wiener filter per resource element (RE):
        \\hat{x} = \\frac{\\mathbf{h}^H \\mathbf{y}}{\\|\\mathbf{h}\\|^2 + N_0}

    Demaps equalized symbols to soft LLRs \\ell_A for QAM constellation.

    Parameters
    ----------
    y : torch.Tensor
        Received OFDM resource grid. Supports 4D [B, rx_ant, T, F] or
        5D [B, 1, rx_ant, T, F].
    h_hat : torch.Tensor
        Channel matrix response. Supports 4D [B, rx_ant, T, F], 5D [B, rx_ant, tx, T, F],
        5D [B, 1, rx_ant, T, F], or 7D [B, 1, rx_ant, 1, 1, T, F_eff].
    no : float or torch.Tensor
        Noise power spectral density N0.
    num_bits_per_symbol : int, optional
        Number of bits per QAM symbol (default: loaded from link_config).
    link_config : LinkConfig, optional
        Physical layer link configuration (default: LinkConfig.from_config()).
    err_var : float or torch.Tensor, optional
        Channel estimation error variance (default: 0.0).
    data_only : bool, optional
        If True (default) and grid matches link_config, extracts data subcarriers
        and data symbols, returning LLR tensor of shape (B, 1, 1, num_data_bits).
        If False, equalizes every RE across the entire grid and returns LLR tensor
        of shape (B, T, F, num_bits_per_symbol).
    resource_grid : ResourceGrid, optional
        Pre-instantiated ResourceGrid instance.
    pilot_seed : int, optional
        Random seed for pilot reference symbols.

    Returns
    -------
    torch.Tensor
        Soft LLRs tensor \\ell_A:
        - If data_only=True: shape (B, 1, 1, num_data_bits)
        - If data_only=False: shape (B, T, F, num_bits_per_symbol)
    """
    if link_config is None:
        link_config = LinkConfig.from_config()

    if num_bits_per_symbol is None:
        num_bits_per_symbol = link_config.num_bits_per_symbol

    # Standardize y dimensions
    if y.ndim == 4:
        y_4d = y
        y_5d = y.unsqueeze(1)
    elif y.ndim == 5:
        y_5d = y
        y_4d = y.squeeze(1)
    else:
        raise ValueError(f"Expected y to be 4D or 5D tensor, got shape {y.shape}")

    device = y.device
    batch_size = y_4d.shape[0]

    # Convert scalar or tensor no / err_var
    if not isinstance(no, torch.Tensor):
        no_tensor = torch.tensor(float(no), dtype=torch.float32, device=device)
    else:
        no_tensor = no.to(device=device, dtype=torch.float32)

    if not isinstance(err_var, torch.Tensor):
        err_var_tensor = torch.tensor(float(err_var), dtype=torch.float32, device=device)
    else:
        err_var_tensor = err_var.to(device=device, dtype=torch.float32)

    is_matching_ofdm_grid = (
        y_4d.shape[-1] == link_config.fft_size and y_4d.shape[-2] == link_config.num_ofdm_symbols
    )

    if data_only and is_matching_ofdm_grid:
        # Route 1: Data-symbols-only demapping matching OFDM codeword layout
        if _SIONNA_AVAILABLE:
            rg = (
                resource_grid
                if resource_grid is not None
                else _get_or_create_resource_grid(link_config, device=device, pilot_seed=pilot_seed)
            )
            sm = StreamManagement(np.array([[1]], dtype=np.int32), 1)
            rem_null = RemoveNulledSubcarriers(rg)
            lmmse_equ = LMMSEEqualizer(rg, sm)
            demapper = Demapper("app", "qam", num_bits_per_symbol)

            # Adapt h_hat to 7D [B, 1, rx_ant, 1, 1, T, F_eff]
            if h_hat.ndim == 7:
                h_7d = h_hat
            elif h_hat.ndim == 6:
                h_7d = h_hat.unsqueeze(1)
            elif h_hat.ndim == 5:
                # [B, rx_ant, tx, T, F] or [B, 1, rx_ant, T, F]
                if h_hat.shape[1] == 1 and h_hat.shape[2] == link_config.num_rx_ant:
                    h_7d_full = h_hat[:, :, :, None, None, :, :]
                else:
                    h_7d_full = h_hat[:, None, :, None, :, :, :]
                if h_7d_full.shape[-1] == link_config.fft_size:
                    h_7d = rem_null(h_7d_full)
                else:
                    h_7d = h_7d_full
            elif h_hat.ndim == 4:
                # [B, rx_ant, T, F]
                h_7d_full = h_hat[:, None, :, None, None, :, :]
                if h_7d_full.shape[-1] == link_config.fft_size:
                    h_7d = rem_null(h_7d_full)
                else:
                    h_7d = h_7d_full
            else:
                raise ValueError(f"Unsupported h_hat shape {h_hat.shape}")

            x_hat, no_eff = lmmse_equ(y_5d, h_7d, err_var_tensor, no_tensor)
            no_eff_ = expand_to_rank(no_eff, x_hat.ndim)
            llr = demapper(x_hat, no_eff_)
            return llr

        else:
            # Route 1 (Fallback): Pure PyTorch OFDM data symbol demapper
            active_sc = _get_active_subcarrier_indices(link_config)
            pilot_syms = set(link_config.pilot_ofdm_symbol_indices)
            data_syms = [t for t in range(link_config.num_ofdm_symbols) if t not in pilot_syms]

            y_eff = y_4d[:, :, :, active_sc]

            # Extract 4D effective h_hat
            if h_hat.ndim == 7:
                h_eff = h_hat[:, 0, :, 0, 0, :, :]
            elif h_hat.ndim == 5:
                if h_hat.shape[-1] == link_config.fft_size:
                    h_eff = h_hat[:, :, 0, :, active_sc] if h_hat.shape[2] == 1 else h_hat.squeeze(1)[:, :, :, active_sc]
                else:
                    h_eff = h_hat[:, :, 0, :, :] if h_hat.shape[2] == 1 else h_hat.squeeze(1)
            elif h_hat.ndim == 4:
                if h_hat.shape[-1] == link_config.fft_size:
                    h_eff = h_hat[:, :, :, active_sc]
                else:
                    h_eff = h_hat
            else:
                raise ValueError(f"Unsupported h_hat shape {h_hat.shape}")

            # Normalize err_var_tensor to 3D [B, T, F_eff] or scalar to avoid IndexError
            if err_var_tensor.ndim > 3:
                err_var_3d = err_var_tensor.view(batch_size, -1, y_eff.shape[2], y_eff.shape[3]).mean(dim=1)
            elif err_var_tensor.ndim == 0:
                err_var_3d = err_var_tensor
            else:
                err_var_3d = err_var_tensor

            # Single-tap SIMO Wiener filter per RE
            num = torch.sum(torch.conj(h_eff) * y_eff, dim=1)  # [B, T, F_eff]
            h_pow = torch.sum(torch.abs(h_eff) ** 2, dim=1)  # [B, T, F_eff]
            x_unbiased = num / (h_pow + 1e-12)
            no_eff = (no_tensor + err_var_3d) / (h_pow + 1e-12)  # [B, T, F_eff]

            # Extract data REs across data OFDM symbols
            x_data = x_unbiased[:, data_syms, :].reshape(batch_size, 1, 1, -1)
            no_data = no_eff[:, data_syms, :].reshape(batch_size, 1, 1, -1)

            llr = _pytorch_demap_app(x_data, no_data, num_bits_per_symbol)
            return llr

    # Route 2: Full grid / per-RE demapping (data_only=False or generic tensor shape)
    # Standardize h_hat to 4D [B, rx_ant, T, F] or [B, rx_ant, T, F_eff]
    if h_hat.ndim == 7:
        h_4d = h_hat[:, 0, :, 0, 0, :, :]
    elif h_hat.ndim == 6:
        h_4d = h_hat[:, 0, :, 0, :, :]
    elif h_hat.ndim == 5:
        if h_hat.shape[1] == 1 and h_hat.shape[2] == link_config.num_rx_ant:
            h_4d = h_hat.squeeze(1)
        elif h_hat.shape[2] == 1:
            h_4d = h_hat.squeeze(2)
        else:
            h_4d = h_hat[:, :, 0, :, :]
    elif h_hat.ndim == 4:
        h_4d = h_hat
    else:
        raise ValueError(f"Unsupported h_hat shape {h_hat.shape}")

    num_symbols = y_4d.shape[2]
    fft_size = y_4d.shape[3]

    # Handle subcarrier dimension mismatch between h_4d (e.g. 116) and y_4d (128)
    if h_4d.shape[-1] != y_4d.shape[-1]:
        if (
            h_4d.shape[-1] == link_config.num_effective_subcarriers
            and y_4d.shape[-1] == link_config.fft_size
        ):
            active_sc = _get_active_subcarrier_indices(link_config)
            y_4d_calc = y_4d[:, :, :, active_sc]  # [B, rx_ant, T, F_eff]
            h_4d_calc = h_4d

            if err_var_tensor.ndim > 3:
                err_var_calc = err_var_tensor.view(batch_size, -1, num_symbols, h_4d.shape[-1]).mean(dim=1)
            elif err_var_tensor.ndim == 0:
                err_var_calc = err_var_tensor
            else:
                err_var_calc = err_var_tensor

            num = torch.sum(torch.conj(h_4d_calc) * y_4d_calc, dim=1)  # [B, T, F_eff]
            h_pow = torch.sum(torch.abs(h_4d_calc) ** 2, dim=1)  # [B, T, F_eff]

            x_unbiased = num / (h_pow + 1e-12)  # [B, T, F_eff]
            no_eff = (no_tensor + err_var_calc) / (h_pow + 1e-12)  # [B, T, F_eff]

            if _SIONNA_AVAILABLE:
                demapper = Demapper("app", "qam", num_bits_per_symbol)
                llr_flat = demapper(x_unbiased, no_eff)  # [B, T, F_eff * m]
                llr_eff = llr_flat.view(batch_size, num_symbols, len(active_sc), num_bits_per_symbol)
            else:
                llr_flat = _pytorch_demap_app(x_unbiased, no_eff, num_bits_per_symbol)
                llr_eff = llr_flat.view(batch_size, num_symbols, len(active_sc), num_bits_per_symbol)

            # Pad into full grid [B, T, fft_size, m] with 0.0 at guard and DC null positions
            llr_grid = torch.zeros(
                batch_size, num_symbols, fft_size, num_bits_per_symbol, device=device, dtype=llr_eff.dtype
            )
            llr_grid[:, :, active_sc, :] = llr_eff
            return llr_grid
        else:
            raise ValueError(
                f"Subcarrier mismatch: y has {y_4d.shape[-1]} subcarriers but h_hat has {h_4d.shape[-1]} subcarriers"
            )

    # When h_4d.shape[-1] == y_4d.shape[-1]
    if err_var_tensor.ndim > 3:
        err_var_calc = err_var_tensor.view(batch_size, -1, num_symbols, h_4d.shape[-1]).mean(dim=1)
    elif err_var_tensor.ndim == 0:
        err_var_calc = err_var_tensor
    else:
        err_var_calc = err_var_tensor

    num = torch.sum(torch.conj(h_4d) * y_4d, dim=1)  # [B, T, F]
    h_pow = torch.sum(torch.abs(h_4d) ** 2, dim=1)  # [B, T, F]

    x_unbiased = num / (h_pow + 1e-12)  # [B, T, F]
    no_eff = (no_tensor + err_var_calc) / (h_pow + 1e-12)  # [B, T, F]

    if _SIONNA_AVAILABLE:
        demapper = Demapper("app", "qam", num_bits_per_symbol)
        llr_flat = demapper(x_unbiased, no_eff)  # [B, T, F * m]
        llr_grid = llr_flat.view(batch_size, num_symbols, fft_size, num_bits_per_symbol)
        return llr_grid
    else:
        llr_flat = _pytorch_demap_app(x_unbiased, no_eff, num_bits_per_symbol)
        llr_grid = llr_flat.view(batch_size, num_symbols, fft_size, num_bits_per_symbol)
        return llr_grid


def b0_receiver(
    Y: torch.Tensor,
    no: Union[float, torch.Tensor],
    link_config: Optional[LinkConfig] = None,
    interpolation_type: str = "nn",
    resource_grid: Optional[Any] = None,
    pilot_seed: Optional[int] = None,
) -> Tuple[torch.Tensor, torch.Tensor]:
    """Baseline B0 receiver: LS channel estimation with interpolation + LMMSE demapper.

    Parameters
    ----------
    Y : torch.Tensor
        Received post-FFT OFDM grid, shape (B, rx_ant, T, F) or (B, 1, rx_ant, T, F).
    no : float or torch.Tensor
        Noise power spectral density N0.
    link_config : LinkConfig, optional
        Physical layer link configuration (default: LinkConfig.from_config()).
    interpolation_type : str, optional
        Channel estimator interpolation mode ('nn' for nearest-neighbor, default).
    resource_grid : ResourceGrid, optional
        Pre-instantiated ResourceGrid instance.
    pilot_seed : int, optional
        Random seed for pilot reference symbols.

    Returns
    -------
    Tuple[torch.Tensor, torch.Tensor]
        - llr: Soft LLRs tensor of shape (B, 1, 1, num_data_bits).
        - h_hat: Estimated channel matrix response from LS estimator.
    """
    if link_config is None:
        link_config = LinkConfig.from_config()

    Y_5d = Y if Y.ndim == 5 else Y.unsqueeze(1)
    rg = (
        resource_grid
        if resource_grid is not None
        else _get_or_create_resource_grid(link_config, device=Y.device, pilot_seed=pilot_seed)
    )

    if _SIONNA_AVAILABLE:
        ls_est = LSChannelEstimator(rg, interpolation_type=interpolation_type)
        h_hat, err_var = ls_est(Y_5d, no)
    else:
        h_hat, err_var = _pytorch_ls_channel_estimator(
            Y_5d,
            link_config,
            interpolation_type=interpolation_type,
            no=no,
            resource_grid=rg,
            pilot_seed=pilot_seed,
        )

    llr = demap_lmmse(
        Y_5d,
        h_hat,
        no,
        num_bits_per_symbol=link_config.num_bits_per_symbol,
        link_config=link_config,
        err_var=err_var,
        data_only=True,
        resource_grid=rg,
        pilot_seed=pilot_seed,
    )

    return llr, h_hat


def b1_receiver(
    Y: torch.Tensor,
    H: torch.Tensor,
    no: Union[float, torch.Tensor],
    link_config: Optional[LinkConfig] = None,
    resource_grid: Optional[Any] = None,
    pilot_seed: Optional[int] = None,
) -> torch.Tensor:
    """Baseline B1 receiver: Perfect CSI (genie-aided) + LMMSE demapper.

    Parameters
    ----------
    Y : torch.Tensor
        Received post-FFT OFDM grid, shape (B, rx_ant, T, F) or (B, 1, rx_ant, T, F).
    H : torch.Tensor
        Perfect CSI channel response, shape (B, rx_ant, tx, T, F) or
        (B, 1, rx_ant, 1, 1, T, F) or (B, rx_ant, T, F).
    no : float or torch.Tensor
        Noise power spectral density N0.
    link_config : LinkConfig, optional
        Physical layer link configuration (default: LinkConfig.from_config()).
    resource_grid : ResourceGrid, optional
        Pre-instantiated ResourceGrid instance.
    pilot_seed : int, optional
        Random seed for pilot reference symbols.

    Returns
    -------
    torch.Tensor
        Soft LLRs tensor of shape (B, 1, 1, num_data_bits).
    """
    if link_config is None:
        link_config = LinkConfig.from_config()

    llr = demap_lmmse(
        Y,
        H,
        no,
        num_bits_per_symbol=link_config.num_bits_per_symbol,
        link_config=link_config,
        err_var=0.0,
        data_only=True,
        resource_grid=resource_grid,
        pilot_seed=pilot_seed,
    )

    return llr
