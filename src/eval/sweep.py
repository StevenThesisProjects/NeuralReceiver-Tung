"""BLER/BER SNR sweep and Clopper-Pearson confidence interval module.

Provides Monte Carlo link-level evaluation pipelines:
- clopper_pearson: Exact 95% binomial confidence intervals via Beta distribution quantiles.
- PointResult: Dataclass recording BLER, BER, confidence bounds, and error tallies.
- bler_point: Single-point Monte Carlo evaluation with early stopping criteria.
- sweep_bler: Multi-point SNR sweep across operating Eb/N0 values.
- plot_bler_curve: Visualization with semilog-y error bars and shaded confidence bands.
- run_b0_cdlc_benchmark: 1-command benchmark for B0 receiver on CDL-C channel profile.
"""

from __future__ import annotations

import math
import os
from dataclasses import asdict, dataclass
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import numpy as np
import torch

from src.config import load_config
from src.rx.classical import b0_receiver, b1_receiver
from src.sim.channels import make_cdl
from src.sim.link import LinkConfig, batch_generator

try:
    from scipy.stats import beta

    _SCIPY_BETA_AVAILABLE = True
except ImportError:
    _SCIPY_BETA_AVAILABLE = False


# ==============================================================================
# 1. Clopper-Pearson Exact Binomial Confidence Intervals
# ==============================================================================


def clopper_pearson(k: int, n: int, alpha: float = 0.05) -> Tuple[float, float]:
    """Calculate exact two-sided Clopper-Pearson confidence interval for a binomial proportion.

    Parameters
    ----------
    k : int
        Number of observed successes/errors.
    n : int
        Total number of trials/blocks.
    alpha : float, optional
        Significance level (default 0.05 for 95% confidence interval).

    Returns
    -------
    Tuple[float, float]
        (ci_low, ci_high) satisfying 0.0 <= ci_low <= k/n <= ci_high <= 1.0.
    """
    if n <= 0:
        return 0.0, 1.0

    k = max(0, min(int(k), int(n)))
    n = int(n)
    alpha = float(alpha)
    half_alpha = alpha / 2.0

    if k == 0:
        ci_low = 0.0
        ci_high = float(1.0 - half_alpha ** (1.0 / n))
    elif k == n:
        ci_low = float(half_alpha ** (1.0 / n))
        ci_high = 1.0
    else:
        if _SCIPY_BETA_AVAILABLE:
            ci_low = float(beta.ppf(half_alpha, k, n - k + 1))
            ci_high = float(beta.ppf(1.0 - half_alpha, k + 1, n - k))
        else:
            # Wilson score interval fallback if scipy is not available
            p = float(k) / float(n)
            z = 1.959963984540054  # 95% quantile
            denom = 1.0 + (z**2) / n
            center = (p + (z**2) / (2.0 * n)) / denom
            half_width = (z * math.sqrt((p * (1.0 - p)) / n + (z**2) / (4.0 * (n**2)))) / denom
            ci_low = max(0.0, center - half_width)
            ci_high = min(1.0, center + half_width)

    p_hat = float(k) / float(n)
    ci_low = max(0.0, min(ci_low, p_hat))
    ci_high = min(1.0, max(ci_high, p_hat))

    return ci_low, ci_high


# ==============================================================================
# 2. PointResult Container
# ==============================================================================


@dataclass
class PointResult:
    """Evaluation result at a single SNR (Eb/N0) operating point.

    Supports both dataclass attribute access (res.bler) and dictionary
    indexing (res['bler']).
    """

    ebno_db: float
    bler: float
    bler_ci_low: float
    bler_ci_high: float
    ber: float
    ber_ci_low: float
    ber_ci_high: float
    block_errors: int
    total_blocks: int
    bit_errors: int
    total_bits: int

    def __getitem__(self, key: str) -> Any:
        if hasattr(self, key):
            return getattr(self, key)
        raise KeyError(f"Invalid PointResult key: '{key}'")

    def to_dict(self) -> Dict[str, Any]:
        """Convert container to python dictionary."""
        return asdict(self)


# ==============================================================================
# 3. Receiver Dispatch Helper
# ==============================================================================


def _execute_rx(
    rx: Union[str, Callable[..., Any]],
    batch: Any,
    link_config: LinkConfig,
) -> torch.Tensor:
    """Execute receiver on batch and return soft LLR tensor of shape (B, 1, 1, num_bits)."""
    if isinstance(rx, str):
        rx_name = rx.lower().strip()
        if rx_name in ("b0", "baseline-ls-estimation", "baseline_ls_estimation", "ls"):
            llr, _ = b0_receiver(Y=batch.Y, no=batch.N0, link_config=link_config)
            return llr
        elif rx_name in ("b1", "baseline-perfect-csi", "baseline_perfect_csi", "genie", "perfect"):
            llr = b1_receiver(Y=batch.Y, H=batch.H, no=batch.N0, link_config=link_config)
            return llr
        else:
            raise ValueError(
                f"Unknown receiver name: '{rx}'. Expected 'b0', 'b1', "
                f"'baseline-ls-estimation', 'baseline-perfect-csi', or callable."
            )
    elif callable(rx):
        try:
            res = rx(Y=batch.Y, no=batch.N0, link_config=link_config)
        except TypeError:
            try:
                res = rx(batch.Y, batch.N0, link_config)
            except TypeError:
                try:
                    res = rx(batch.Y, batch.N0)
                except TypeError:
                    try:
                        res = rx(batch.Y, batch.H, batch.N0, link_config=link_config)
                    except TypeError:
                        res = rx(batch)

        if isinstance(res, (tuple, list)):
            return res[0]
        return res
    else:
        raise TypeError(f"Receiver must be a string identifier or callable, got {type(rx).__name__}")


# ==============================================================================
# 4. Single SNR Point Evaluation: bler_point
# ==============================================================================


def bler_point(
    rx: Union[str, Callable[..., Any]],
    ebno_db: float,
    channel: Optional[Any] = None,
    link_config: Optional[LinkConfig] = None,
    target_errors: Optional[int] = None,
    max_slots: Optional[int] = None,
    batch_size: Optional[int] = None,
    seed: Optional[int] = None,
    device: Optional[Union[str, torch.device]] = None,
    alpha: float = 0.05,
) -> PointResult:
    """Evaluate Block Error Rate (BLER) and Bit Error Rate (BER) at a single Eb/N0 point.

    Employs early-stopping: terminates as soon as `block_errors >= target_errors`
    OR `total_blocks >= max_slots`.

    Parameters
    ----------
    rx : str or callable
        Receiver implementation ('b0', 'b1', or callable returning LLR tensor).
    ebno_db : float
        Operating Eb/N0 point in dB.
    channel : Any, optional
        Channel instance (defaults to make_cdl() from config).
    link_config : LinkConfig, optional
        Physical layer link configuration (defaults to LinkConfig.from_config()).
    target_errors : int, optional
        Target number of block errors for early stopping (default 100 from config).
    max_slots : int, optional
        Maximum number of slots/blocks to simulate (default 50,000).
    batch_size : int, optional
        Batch size per Monte Carlo iteration (default 128 from config).
    seed : int, optional
        Base random seed for batch generator determinism.
    device : str or torch.device, optional
        Computation device.
    alpha : float, optional
        Significance level for Clopper-Pearson CI (default 0.05 -> 95% CI).

    Returns
    -------
    PointResult
        Container holding BLER, BER, error counts, and Clopper-Pearson confidence bounds.
    """
    cfg = load_config()
    eval_cfg = cfg.get("evaluation", {})

    if link_config is None:
        link_config = LinkConfig.from_config()

    if target_errors is None:
        target_errors = int(eval_cfg.get("num_target_block_errors", 100))
    else:
        target_errors = int(target_errors)

    if batch_size is None:
        batch_size = int(eval_cfg.get("batch_size", 128))
    else:
        batch_size = int(batch_size)

    if max_slots is None:
        max_slots = int(eval_cfg.get("max_slots", 50000))
    else:
        max_slots = int(max_slots)

    if channel is None:
        channel = make_cdl()

    base_seed = int(seed) if seed is not None else int(cfg.get("seed", 42))

    block_errors = 0
    total_blocks = 0
    bit_errors = 0
    total_bits = 0
    iter_idx = 0

    while total_blocks < max_slots and block_errors < target_errors:
        cur_bs = min(batch_size, max_slots - total_blocks)
        if cur_bs <= 0:
            break

        batch_seed = (base_seed + iter_idx * 1000 + 1) & 0x7FFFFFFF

        batch = batch_generator(
            channel=channel,
            link_config=link_config,
            batch_size=cur_bs,
            ebno_db=float(ebno_db),
            seed=batch_seed,
            device=device,
        )

        llr = _execute_rx(rx, batch, link_config)
        b_hat = (llr > 0.0).to(batch.b.dtype)

        # Flatten per-slot bits: shape [cur_bs, -1]
        b_flat = batch.b.view(cur_bs, -1)
        b_hat_flat = b_hat.view(cur_bs, -1)

        bit_diff = (b_flat != b_hat_flat)
        cur_bit_errors = int(bit_diff.sum().item())
        cur_block_errors = int((bit_diff.sum(dim=-1) > 0).sum().item())

        bit_errors += cur_bit_errors
        block_errors += cur_block_errors
        total_blocks += cur_bs
        total_bits += b_flat.numel()

        iter_idx += 1

    bler = float(block_errors) / float(max(1, total_blocks))
    bler_ci_low, bler_ci_high = clopper_pearson(block_errors, total_blocks, alpha=alpha)

    ber = float(bit_errors) / float(max(1, total_bits))
    ber_ci_low, ber_ci_high = clopper_pearson(bit_errors, total_bits, alpha=alpha)

    return PointResult(
        ebno_db=float(ebno_db),
        bler=bler,
        bler_ci_low=bler_ci_low,
        bler_ci_high=bler_ci_high,
        ber=ber,
        ber_ci_low=ber_ci_low,
        ber_ci_high=ber_ci_high,
        block_errors=block_errors,
        total_blocks=total_blocks,
        bit_errors=bit_errors,
        total_bits=total_bits,
    )


# ==============================================================================
# 5. Multi-Point SNR Sweep: sweep_bler
# ==============================================================================


def sweep_bler(
    rx: Union[str, Callable[..., Any]],
    ebno_dbs: Optional[Union[List[float], np.ndarray, torch.Tensor]] = None,
    channel: Optional[Any] = None,
    link_config: Optional[LinkConfig] = None,
    target_errors: Optional[int] = None,
    max_slots: Optional[int] = None,
    batch_size: Optional[int] = None,
    seed: Optional[int] = None,
    device: Optional[Union[str, torch.device]] = None,
    alpha: float = 0.05,
    verbose: bool = True,
) -> List[PointResult]:
    """Execute SNR sweep across multiple Eb/N0 operating points.

    Parameters
    ----------
    rx : str or callable
        Receiver implementation.
    ebno_dbs : list, ndarray, or tensor, optional
        Array of Eb/N0 values in dB (defaults to evaluation range in config).
    channel : Any, optional
        Shared channel instance.
    link_config : LinkConfig, optional
        Physical layer link configuration.
    target_errors : int, optional
        Block error target for early stopping.
    max_slots : int, optional
        Maximum slot ceiling.
    batch_size : int, optional
        Batch size per iteration.
    seed : int, optional
        Base random seed.
    device : str or torch.device, optional
        Device for computation.
    alpha : float, optional
        Significance level for CI calculation (default 0.05).
    verbose : bool, optional
        Print iteration progress log to stdout (default True).

    Returns
    -------
    List[PointResult]
        List of PointResult instances for each evaluated SNR point.
    """
    if ebno_dbs is None:
        cfg = load_config()
        eval_cfg = cfg.get("evaluation", {})
        ebno_db_min = float(eval_cfg.get("ebno_db_min", 0.0))
        ebno_db_max = float(eval_cfg.get("ebno_db_max", 20.0))
        ebno_db_step = float(eval_cfg.get("ebno_db_step", 2.0))
        ebno_dbs_list = list(np.arange(ebno_db_min, ebno_db_max + ebno_db_step / 2.0, ebno_db_step))
    elif isinstance(ebno_dbs, (torch.Tensor, np.ndarray)):
        ebno_dbs_list = [float(x) for x in ebno_dbs.tolist()]
    else:
        ebno_dbs_list = [float(x) for x in ebno_dbs]

    if channel is None:
        channel = make_cdl()

    results: List[PointResult] = []

    for snr in ebno_dbs_list:
        pt = bler_point(
            rx=rx,
            ebno_db=snr,
            channel=channel,
            link_config=link_config,
            target_errors=target_errors,
            max_slots=max_slots,
            batch_size=batch_size,
            seed=seed,
            device=device,
            alpha=alpha,
        )
        results.append(pt)

        if verbose:
            print(
                f"[Eb/N0 = {pt.ebno_db:5.1f} dB] "
                f"BLER: {pt.bler:9.4e} (95% CI: [{pt.bler_ci_low:.4e}, {pt.bler_ci_high:.4e}]) | "
                f"BER: {pt.ber:9.4e} | "
                f"Errors: {pt.block_errors:4d} / {pt.total_blocks:6d} slots"
            )

    return results


# ==============================================================================
# 6. Visualization: plot_bler_curve
# ==============================================================================


def plot_bler_curve(
    results: Union[List[PointResult], Dict[str, List[PointResult]]],
    save_path: Optional[str] = None,
    title: Optional[str] = None,
    show_ci: bool = True,
    show_ber: bool = False,
    ax: Optional[Any] = None,
) -> Any:
    """Plot BLER (and optional BER) performance curves with Clopper-Pearson 95% CIs.

    Parameters
    ----------
    results : List[PointResult] or Dict[str, List[PointResult]]
        Single result list or dictionary mapping label to result list.
    save_path : str, optional
        Target filepath to save plot artifact.
    title : str, optional
        Plot title.
    show_ci : bool, optional
        Display error bars and shaded confidence bands (default True).
    show_ber : bool, optional
        Also display bit error rate curves (default False).
    ax : matplotlib.axes.Axes, optional
        Existing axes to draw on.

    Returns
    -------
    matplotlib.figure.Figure or matplotlib.axes.Axes
        Plot handle.
    """
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 6))
        standalone = True
    else:
        fig = ax.figure
        standalone = False

    if isinstance(results, list):
        curves: Dict[str, List[PointResult]] = {"BLER": results}
    else:
        curves = results

    for label, pts in curves.items():
        if not pts:
            continue
        pts_sorted = sorted(pts, key=lambda p: p.ebno_db)
        ebno_vals = np.array([p.ebno_db for p in pts_sorted], dtype=np.float64)
        bler_vals = np.array([p.bler for p in pts_sorted], dtype=np.float64)
        ci_lows = np.array([p.bler_ci_low for p in pts_sorted], dtype=np.float64)
        ci_highs = np.array([p.bler_ci_high for p in pts_sorted], dtype=np.float64)

        # Plot BLER line with markers
        line = ax.semilogy(ebno_vals, bler_vals, marker="o", linewidth=2.0, label=label)
        color = line[0].get_color()

        if show_ci:
            ci_floor = 1e-6
            cl_clamped = np.maximum(ci_lows, ci_floor)
            ch_clamped = np.maximum(ci_highs, ci_floor)
            ax.fill_between(ebno_vals, cl_clamped, ch_clamped, color=color, alpha=0.18)

            yerr_low = np.maximum(0.0, bler_vals - np.maximum(ci_lows, 1e-7))
            yerr_high = np.maximum(0.0, ci_highs - bler_vals)
            ax.errorbar(
                ebno_vals,
                bler_vals,
                yerr=[yerr_low, yerr_high],
                fmt="none",
                ecolor=color,
                elinewidth=1.2,
                capsize=3,
                alpha=0.8,
            )

        if show_ber:
            ber_vals = np.array([p.ber for p in pts_sorted], dtype=np.float64)
            ax.semilogy(
                ebno_vals,
                ber_vals,
                marker="s",
                linestyle="--",
                linewidth=1.5,
                color=color,
                alpha=0.7,
                label=f"{label} (BER)",
            )

    ax.set_xlabel(r"$E_b/N_0$ [dB]", fontsize=12)
    ax.set_ylabel("Error Rate", fontsize=12)
    ax.set_title(title or "BLER Performance with Clopper-Pearson 95% CI", fontsize=13)
    ax.grid(True, which="both", linestyle="--", alpha=0.5)
    ax.legend(loc="lower left", fontsize=11)

    if save_path is not None:
        os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)
        fig.savefig(save_path, dpi=300, bbox_inches="tight")

    if standalone:
        return fig, ax
    return ax


# ==============================================================================
# 7. One-Command Benchmark Runner: run_b0_cdlc_benchmark
# ==============================================================================


def run_b0_cdlc_benchmark(
    v: float = 10.0,
    ebno_dbs: Optional[Union[List[float], np.ndarray]] = None,
    save_path: str = "plots/evaluation/b0_cdlc_10ms_bler.png",
    target_errors: Optional[int] = None,
    max_slots: Optional[int] = None,
    batch_size: Optional[int] = None,
    verbose: bool = True,
) -> List[PointResult]:
    """Execute 1-command benchmark for Baseline B0 receiver over CDL-C at speed v.

    Satisfies Issue #3 DoD: 'Đường B0 tại CDL-C, 10 m/s, 64-QAM R = 0.9 vẽ được bằng 1 lệnh'.

    Parameters
    ----------
    v : float, optional
        UE velocity in m/s (default 10.0).
    ebno_dbs : list or ndarray, optional
        Array of Eb/N0 values in dB (defaults to [8.0, 10.0, 12.0, 14.0, 16.0, 18.0, 20.0]).
    save_path : str, optional
        Target filepath to save plot artifact (default 'plots/evaluation/b0_cdlc_10ms_bler.png').
    target_errors : int, optional
        Block error target for early stopping.
    max_slots : int, optional
        Maximum slot ceiling.
    batch_size : int, optional
        Batch size per iteration.
    verbose : bool, optional
        Print iteration logs to stdout (default True).

    Returns
    -------
    List[PointResult]
        List of PointResult instances for evaluated SNR points.
    """
    channel = make_cdl(model="C", v=v)
    link_config = LinkConfig.from_config()

    if ebno_dbs is None:
        ebno_dbs = [8.0, 10.0, 12.0, 14.0, 16.0, 18.0, 20.0]

    results = sweep_bler(
        rx="b0",
        ebno_dbs=ebno_dbs,
        channel=channel,
        link_config=link_config,
        target_errors=target_errors,
        max_slots=max_slots,
        batch_size=batch_size,
        verbose=verbose,
    )

    plot_bler_curve(
        results,
        save_path=save_path,
        title=f"Baseline B0 (LS-LMMSE) on CDL-C (v = {v:.1f} m/s, 64-QAM, R = {link_config.coderate})",
        show_ci=True,
    )

    return results
