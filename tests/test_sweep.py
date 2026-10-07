"""Unit test suite for BLER SNR sweep and Clopper-Pearson 95% confidence intervals.

Verifies:
1. Exact Clopper-Pearson binomial confidence interval bounds (test_ci_bounds).
2. Monte Carlo early stopping criteria on target_errors and max_slots (test_bler_point_stopping_criteria).
3. Multi-point SNR sweep execution and BLER monotonicity (test_sweep_execution).
4. Semilog-y error bar and shaded CI plotting to artifact files (test_plot_bler_curve_generates_file).
5. One-command benchmark runner for B0 on CDL-C (test_run_b0_cdlc_benchmark_smoke).
"""

from __future__ import annotations

import os
import pytest
import torch

from src.eval.sweep import (
    PointResult,
    bler_point,
    clopper_pearson,
    plot_bler_curve,
    run_b0_cdlc_benchmark,
    sweep_bler,
)
from src.sim.channels import make_cdl
from src.sim.link import LinkConfig


def test_ci_bounds():
    """Verify exact Clopper-Pearson 95% confidence interval formulas and bounds."""
    # Boundary: k = 0, n = 100 -> CI_low = 0.0, CI_high ≈ 0.0362
    low0, high0 = clopper_pearson(0, 100, alpha=0.05)
    assert low0 == 0.0, f"Expected low=0.0, got {low0}"
    assert abs(high0 - 0.0362) < 0.001, f"Expected high≈0.0362, got {high0}"
    assert 0.0 <= low0 <= (0 / 100) <= high0 <= 1.0

    # Boundary: k = 100, n = 100 -> CI_low ≈ 0.9638, CI_high = 1.0
    low100, high100 = clopper_pearson(100, 100, alpha=0.05)
    assert abs(low100 - 0.9638) < 0.001, f"Expected low≈0.9638, got {low100}"
    assert high100 == 1.0, f"Expected high=1.0, got {high100}"
    assert 0.0 <= low100 <= (100 / 100) <= high100 <= 1.0

    # Interior: k = 50, n = 100 -> CI_low ≈ 0.3983, CI_high ≈ 0.6017
    low50, high50 = clopper_pearson(50, 100, alpha=0.05)
    assert abs(low50 - 0.3983) < 0.001, f"Expected low≈0.3983, got {low50}"
    assert abs(high50 - 0.6017) < 0.001, f"Expected high≈0.6017, got {high50}"
    assert 0.0 <= low50 <= (50 / 100) <= high50 <= 1.0

    # Edge cases: n <= 0
    assert clopper_pearson(0, 0) == (0.0, 1.0)
    assert clopper_pearson(5, -1) == (0.0, 1.0)


def test_bler_point_stopping_criteria():
    """Verify bler_point terminates promptly on target_errors or max_slots."""
    cfg = LinkConfig.from_config()
    chan = make_cdl(model="C", v=0.0)

    # Condition 1: Early stop on target_errors
    # At Eb/N0 = 0.0 dB, error rate is high; should stop when block_errors >= 3
    res_err = bler_point(
        rx="b0",
        ebno_db=0.0,
        channel=chan,
        link_config=cfg,
        target_errors=3,
        max_slots=50,
        batch_size=2,
        seed=42,
    )
    assert res_err.block_errors >= 3, f"Expected >= 3 errors, got {res_err.block_errors}"
    assert res_err.total_blocks < 50, f"Expected early stop before 50 slots, got {res_err.total_blocks}"
    assert 0.0 <= res_err.bler_ci_low <= res_err.bler <= res_err.bler_ci_high <= 1.0

    # Condition 2: Early stop on max_slots ceiling
    # At Eb/N0 = 25.0 dB, errors are zero/low; should stop when total_blocks reaches max_slots=6
    res_max = bler_point(
        rx="b0",
        ebno_db=25.0,
        channel=chan,
        link_config=cfg,
        target_errors=100,
        max_slots=6,
        batch_size=2,
        seed=42,
    )
    assert res_max.total_blocks == 6, f"Expected exactly 6 slots, got {res_max.total_blocks}"
    assert res_max.block_errors < 100, f"Expected errors < 100, got {res_max.block_errors}"
    assert 0.0 <= res_max.bler_ci_low <= res_max.bler <= res_max.bler_ci_high <= 1.0


def test_sweep_execution():
    """Verify multi-point SNR sweep execution, result structure, and BLER monotonicity."""
    cfg = LinkConfig.from_config()
    chan = make_cdl(model="C", v=0.0)

    results = sweep_bler(
        rx="b0",
        ebno_dbs=[10.0, 20.0],
        channel=chan,
        link_config=cfg,
        target_errors=2,
        max_slots=4,
        batch_size=2,
        seed=42,
        verbose=False,
    )

    assert len(results) == 2, f"Expected 2 points, got {len(results)}"
    pt10, pt20 = results[0], results[1]

    # Verify PointResult attributes & dictionary access
    assert pt10.ebno_db == 10.0
    assert pt20.ebno_db == 20.0
    assert pt10["bler"] == pt10.bler
    assert pt10["ebno_db"] == 10.0
    assert isinstance(pt10.to_dict(), dict)

    # Monotonicity: Higher SNR has lower or equal BLER
    assert pt20.bler <= pt10.bler, f"BLER should decrease with SNR: {pt20.bler} vs {pt10.bler}"
    assert pt20.ber <= pt10.ber, f"BER should decrease with SNR: {pt20.ber} vs {pt10.ber}"


def test_plot_bler_curve_generates_file(tmp_path):
    """Verify plot_bler_curve creates valid PNG file with error bars and confidence bands."""
    pts = [
        PointResult(
            ebno_db=10.0,
            bler=1.0,
            bler_ci_low=0.2,
            bler_ci_high=1.0,
            ber=0.03,
            ber_ci_low=0.02,
            ber_ci_high=0.04,
            block_errors=2,
            total_blocks=2,
            bit_errors=20,
            total_bits=200,
        ),
        PointResult(
            ebno_db=20.0,
            bler=0.0,
            bler_ci_low=0.0,
            bler_ci_high=0.6,
            ber=0.0,
            ber_ci_low=0.0,
            ber_ci_high=0.01,
            block_errors=0,
            total_blocks=4,
            bit_errors=0,
            total_bits=400,
        ),
    ]

    out_file = str(tmp_path / "bler_curve_test.png")
    plot_bler_curve(pts, save_path=out_file, title="Test BLER Curve", show_ci=True, show_ber=True)

    assert os.path.exists(out_file), "Plot artifact was not created"
    assert os.path.getsize(out_file) > 1000, "Plot file size is unexpectedly small"

    # Also verify dictionary input for multiple curves
    out_multi = str(tmp_path / "bler_multi_curve_test.png")
    plot_bler_curve({"B0 (LS)": pts, "B1 (Genie)": pts}, save_path=out_multi, show_ci=True)
    assert os.path.exists(out_multi)
    assert os.path.getsize(out_multi) > 1000


def test_run_b0_cdlc_benchmark_smoke(tmp_path):
    """Verify 1-command benchmark runner runs cleanly and saves plot artifact."""
    bench_file = str(tmp_path / "bench_b0_cdlc.png")
    res = run_b0_cdlc_benchmark(
        v=10.0,
        ebno_dbs=[15.0],
        save_path=bench_file,
        target_errors=1,
        max_slots=2,
        batch_size=2,
        verbose=False,
    )

    assert len(res) == 1
    assert isinstance(res[0], PointResult)
    assert res[0].ebno_db == 15.0
    assert os.path.exists(bench_file), "Benchmark plot artifact was not created"
    assert os.path.getsize(bench_file) > 1000
