"""Unit tests for simulation modules (channels.py and link.py)."""

import math
import numpy as np
import pytest
import torch

from src.sim import LinkConfig, SyntheticCDL, batch_generator, make_cdl


def test_cdl_seed_determinism():
    """Verify deterministic channel impulse response generation for identical seeds."""
    seed = 1234
    cdl1 = make_cdl(seed=seed)
    cdl2 = make_cdl(seed=seed)

    # Generate CIR with fixed parameters
    a1, tau1 = cdl1(batch_size=2, num_time_steps=14, sampling_frequency=128 * 30000.0)
    a2, tau2 = cdl2(batch_size=2, num_time_steps=14, sampling_frequency=128 * 30000.0)

    assert torch.allclose(a1, a2), f"Path coefficients differ: max diff = {torch.max(torch.abs(a1 - a2)).item()}"
    assert torch.allclose(tau1, tau2), f"Path delays differ: max diff = {torch.max(torch.abs(tau1 - tau2)).item()}"


def test_shapes():
    """Verify output tensor shapes from batch_generator match physical specification."""
    cfg = LinkConfig.from_config()
    batch = batch_generator(link_config=cfg, batch_size=2)
    b, Y, X_pilot, N0, H = batch

    # Validate Y shape: (batch_size, num_rx_ant, num_ofdm_symbols, fft_size)
    assert Y.shape == (2, 2, 14, 128), f"Expected Y shape (2, 2, 14, 128), got {Y.shape}"

    # Validate H shape: (batch_size, num_rx_ant, num_tx, num_ofdm_symbols, fft_size)
    assert H.shape == (2, 2, 1, 14, 128), f"Expected H shape (2, 2, 1, 14, 128), got {H.shape}"

    # Validate N0 is a positive scalar
    assert float(N0) > 0.0, f"Expected positive N0, got {N0}"

    # Validate b shape: (batch_size, num_tx, 1, num_data_bits)
    assert b.shape[0] == 2
    assert b.shape[1] == cfg.num_tx_ant
    assert b.shape[2] == 1
    assert b.shape[3] == cfg.num_data_bits

    # Validate X_pilot is not empty
    assert X_pilot is not None
    assert X_pilot.numel() > 0


def test_link_config_from_config():
    """Verify LinkConfig loads parameters correctly from config.yaml."""
    cfg = LinkConfig.from_config()
    assert cfg.fft_size == 128
    assert cfg.num_ofdm_symbols == 14
    assert cfg.subcarrier_spacing == 30000.0
    assert cfg.carrier_frequency == 3.5e9
    assert cfg.num_tx_ant == 1
    assert cfg.num_rx_ant == 2
    assert cfg.pilot_ofdm_symbol_indices == [2, 11]
    assert cfg.num_guard_carriers == [5, 6]
    assert cfg.dc_null is True
    assert cfg.num_bits_per_symbol == 6
    assert abs(cfg.coderate - 0.9) < 1e-6
    assert cfg.num_effective_subcarriers == 116
    assert cfg.num_data_symbols == 1392
    assert cfg.num_data_bits == 8352
    assert cfg.k == int(8352 * 0.9)


def test_synthetic_cdl_determinism():
    """Verify SyntheticCDL fallback behaves deterministically and generates correct shapes."""
    syn1 = SyntheticCDL(seed=777)
    syn2 = SyntheticCDL(seed=777)

    h1, tau1 = syn1(batch_size=3, num_time_steps=14, sampling_frequency=128 * 30000.0)
    h2, tau2 = syn2(batch_size=3, num_time_steps=14, sampling_frequency=128 * 30000.0)

    assert torch.allclose(h1, h2), "SyntheticCDL impulse response must be deterministic"
    assert torch.allclose(tau1, tau2), "SyntheticCDL delays must be deterministic"
    assert h1.shape == (3, 1, 2, 1, 1, 24, 14)
