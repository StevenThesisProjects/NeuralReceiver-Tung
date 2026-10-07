"""Unit tests for classical baseline receivers (b0_receiver, b1_receiver, demap_lmmse)."""

import math
from unittest.mock import patch
import numpy as np
import pytest
import torch

from src.rx import b0_receiver, b1_receiver, demap_lmmse
import src.rx.classical as classical_mod
from src.rx.classical import _get_active_subcarrier_indices
from src.sim.link import LinkConfig, batch_generator


def test_b0_matches_sionna():
    """Verify B0 receiver on batch from batch_generator at 15 dB.

    Verifies output shapes, finite LLR values, and that BER < 0.05.
    Note: In Sionna/PyTorch logits convention, LLR > 0 corresponds to bit 1,
    matching binary_cross_entropy_with_logits.
    """
    link_config = LinkConfig.from_config()
    batch = batch_generator(link_config=link_config, batch_size=2, ebno_db=15.0, seed=42)
    b, Y, X_pilot, N0, H = batch

    llr, h_hat = b0_receiver(Y, N0, link_config=link_config)

    # 1. Output shapes
    expected_shape = (2, 1, 1, link_config.num_data_bits)
    assert llr.shape == expected_shape, f"Expected LLR shape {expected_shape}, got {llr.shape}"
    assert h_hat is not None, "h_hat should not be None"

    # 2. Finite LLR values (no NaN or Inf)
    assert torch.all(torch.isfinite(llr)), "LLR contains non-finite values (NaN or Inf)"

    # 3. Hard-decision BER < 0.05 (strictly verified)
    b_hat = (llr > 0.0).float()
    ber = torch.mean((b != b_hat).float()).item()
    assert ber < 0.05, f"Expected B0 BER < 0.05 at 15 dB, got {ber:.4f}"


def test_b1_superior_to_b0():
    """Verify B1 (perfect CSI) receiver achieves BER <= B0 (LS estimated) at 15 dB."""
    link_config = LinkConfig.from_config()
    batch = batch_generator(link_config=link_config, batch_size=2, ebno_db=15.0, seed=42)
    b, Y, X_pilot, N0, H = batch

    llr_b0, _ = b0_receiver(Y, N0, link_config=link_config)
    llr_b1 = b1_receiver(Y, H, N0, link_config=link_config)

    # 1. Shapes and finiteness
    expected_shape = (2, 1, 1, link_config.num_data_bits)
    assert llr_b1.shape == expected_shape, f"Expected B1 LLR shape {expected_shape}, got {llr_b1.shape}"
    assert torch.all(torch.isfinite(llr_b1)), "B1 LLR contains non-finite values"

    # 2. BER comparison
    b_hat_b0 = (llr_b0 > 0.0).float()
    b_hat_b1 = (llr_b1 > 0.0).float()
    ber_b0 = torch.mean((b != b_hat_b0).float()).item()
    ber_b1 = torch.mean((b != b_hat_b1).float()).item()

    assert ber_b1 <= ber_b0, (
        f"Expected B1 BER ({ber_b1:.4f}) <= B0 BER ({ber_b0:.4f}) at 15 dB"
    )


def test_demap_lmmse_per_re():
    """Verify demap_lmmse with data_only=False produces (B, T, F, m) full-grid LLRs."""
    link_config = LinkConfig.from_config()
    batch = batch_generator(link_config=link_config, batch_size=2, ebno_db=15.0, seed=123)
    b, Y, X_pilot, N0, H = batch

    llr_grid = demap_lmmse(Y, H, N0, link_config=link_config, data_only=False)

    expected_shape = (2, link_config.num_ofdm_symbols, link_config.fft_size, link_config.num_bits_per_symbol)
    assert llr_grid.shape == expected_shape, f"Expected shape {expected_shape}, got {llr_grid.shape}"
    assert torch.all(torch.isfinite(llr_grid)), "Full-grid LLR contains non-finite values"


def test_input_dimension_flexibility():
    """Verify B0 and B1 receivers handle both 4D and 5D inputs interchangeably."""
    link_config = LinkConfig.from_config()
    batch = batch_generator(link_config=link_config, batch_size=2, ebno_db=15.0, seed=42)
    b, Y, X_pilot, N0, H = batch

    # Y is 4D: (2, 2, 14, 128)
    assert Y.ndim == 4
    Y_5d = Y.unsqueeze(1)  # (2, 1, 2, 14, 128)

    llr_b0_4d, _ = b0_receiver(Y, N0, link_config=link_config)
    llr_b0_5d, _ = b0_receiver(Y_5d, N0, link_config=link_config)

    assert torch.allclose(llr_b0_4d, llr_b0_5d, atol=1e-5), "B0 output differs between 4D and 5D Y input"

    llr_b1_4d = b1_receiver(Y, H, N0, link_config=link_config)
    llr_b1_5d = b1_receiver(Y_5d, H, N0, link_config=link_config)

    assert torch.allclose(llr_b1_4d, llr_b1_5d, atol=1e-5), "B1 output differs between 4D and 5D Y input"


def test_pytorch_fallback_receivers():
    """Verify pure PyTorch fallback operates correctly when Sionna is unavailable."""
    link_config = LinkConfig.from_config()
    batch = batch_generator(link_config=link_config, batch_size=2, ebno_db=15.0, seed=42)
    b, Y, X_pilot, N0, H = batch

    with patch.object(classical_mod, "_SIONNA_AVAILABLE", False):
        llr_b0, h_hat_b0 = classical_mod.b0_receiver(Y, N0, link_config=link_config)
        llr_b1 = classical_mod.b1_receiver(Y, H, N0, link_config=link_config)
        llr_grid = classical_mod.demap_lmmse(Y, H, N0, link_config=link_config, data_only=False)

        expected_shape = (2, 1, 1, link_config.num_data_bits)
        assert llr_b0.shape == expected_shape
        assert llr_b1.shape == expected_shape
        assert llr_grid.shape == (2, link_config.num_ofdm_symbols, link_config.fft_size, link_config.num_bits_per_symbol)

        assert torch.all(torch.isfinite(llr_b0))
        assert torch.all(torch.isfinite(llr_b1))
        assert torch.all(torch.isfinite(llr_grid))

        ber_b0 = torch.mean((b != (llr_b0 > 0.0).float()).float()).item()
        ber_b1 = torch.mean((b != (llr_b1 > 0.0).float()).float()).item()

        assert ber_b0 < 0.05, f"Expected fallback B0 BER < 0.05, got {ber_b0:.4f}"
        assert ber_b1 <= ber_b0


def test_b0_arbitrary_seed():
    """Verify B0 receiver achieves BER < 0.05 with arbitrary batch generation seeds."""
    link_config = LinkConfig.from_config()
    for seed_val in [123, 999]:
        batch = batch_generator(link_config=link_config, batch_size=2, ebno_db=15.0, seed=seed_val)
        b, Y, X_pilot, N0, H = batch

        llr, h_hat = b0_receiver(Y, N0, link_config=link_config)
        b_hat = (llr > 0.0).float()
        ber = torch.mean((b != b_hat).float()).item()
        assert ber < 0.05, f"Seed {seed_val}: Expected B0 BER < 0.05 at 15 dB, got {ber:.4f}"


def test_demap_lmmse_with_b0_h_hat_full_grid():
    """Verify demap_lmmse with data_only=False works with h_hat from b0_receiver without dimension mismatch."""
    link_config = LinkConfig.from_config()
    batch = batch_generator(link_config=link_config, batch_size=2, ebno_db=15.0, seed=42)
    b, Y, X_pilot, N0, H = batch

    llr_b0, h_hat_b0 = b0_receiver(Y, N0, link_config=link_config)
    llr_grid = demap_lmmse(Y, h_hat_b0, N0, link_config=link_config, data_only=False)

    expected_shape = (2, link_config.num_ofdm_symbols, link_config.fft_size, link_config.num_bits_per_symbol)
    assert llr_grid.shape == expected_shape, f"Expected shape {expected_shape}, got {llr_grid.shape}"

    # Active subcarriers should have finite non-zero LLRs
    active_sc = _get_active_subcarrier_indices(link_config)
    active_llrs = llr_grid[:, :, active_sc, :]
    assert torch.all(torch.isfinite(active_llrs))
    assert not torch.all(active_llrs == 0.0)

    # Guard carriers and DC null should be exactly 0.0
    guard_sc = [i for i in range(link_config.fft_size) if i not in set(active_sc)]
    guard_llrs = llr_grid[:, :, guard_sc, :]
    assert torch.all(guard_llrs == 0.0), "Guard subcarriers and DC null must be padded with 0.0"
