"""Unit tests for simulation modules (channels.py and link.py)."""

import math
import numpy as np
import pytest
import torch

from src.sim import LinkConfig, SyntheticCDL, SyntheticCDLChannel, batch_generator, make_cdl


def test_cdl_seed_determinism():
    """Verify deterministic channel impulse response and frequency response for identical seeds."""
    seed = 1234
    cdl1 = make_cdl(seed=seed)
    cdl2 = make_cdl(seed=seed)

    # 1. Verify channel attributes
    assert hasattr(cdl1, "seed"), "cdl1 must have 'seed' attribute"
    assert cdl1.seed == seed
    assert hasattr(cdl1, "sample"), "cdl1 must have 'sample' method"

    # 2. CIR determinism
    a1, tau1 = cdl1(batch_size=2, num_time_steps=14, sampling_frequency=cdl1.fft_size * cdl1.subcarrier_spacing)
    a2, tau2 = cdl2(batch_size=2, num_time_steps=14, sampling_frequency=cdl2.fft_size * cdl2.subcarrier_spacing)

    assert torch.allclose(a1, a2), f"Path coefficients differ: max diff = {torch.max(torch.abs(a1 - a2)).item()}"
    assert torch.allclose(tau1, tau2), f"Path delays differ: max diff = {torch.max(torch.abs(tau1 - tau2)).item()}"

    # 3. Frequency response sample() determinism
    cdl1_samp = make_cdl(seed=seed)
    cdl2_samp = make_cdl(seed=seed)
    h1 = cdl1_samp.sample(batch_size=2)
    h2 = cdl2_samp.sample(batch_size=2)

    assert torch.allclose(h1, h2), f"Sampled frequency responses differ: max diff = {torch.max(torch.abs(h1 - h2)).item()}"
    assert h1.shape == (2, 2, 1, 14, 128), f"Expected shape (2, 2, 1, 14, 128), got {h1.shape}"


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
    assert b.shape == (2, cfg.num_tx_ant, 1, cfg.num_data_bits), (
        f"Expected b shape (2, {cfg.num_tx_ant}, 1, {cfg.num_data_bits}), got {b.shape}"
    )

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
    assert cfg.num_tx_antennas == 1
    assert cfg.num_rx_antennas == 2
    assert cfg.pilot_ofdm_symbol_indices == [2, 11]
    assert cfg.num_guard_carriers == [5, 6]
    assert cfg.guard_subcarriers == [5, 6]
    assert cfg.dc_null is True
    assert cfg.num_bits_per_symbol == 6
    assert abs(cfg.coderate - 0.9) < 1e-6
    assert cfg.num_effective_subcarriers == 116
    assert cfg.num_pilot_symbols == 232
    assert cfg.num_data_symbols == 1392
    assert cfg.num_data_bits == 8352
    assert cfg.k == int(8352 * 0.9)
    assert cfg.cdl_model == "C"
    assert abs(cfg.delay_spread - 100e-9) < 1e-12


def test_synthetic_cdl_determinism():
    """Verify SyntheticCDLChannel fallback behaves deterministically and generates correct shapes."""
    syn1 = SyntheticCDLChannel(seed=777)
    syn2 = SyntheticCDLChannel(seed=777)

    assert syn1.seed == 777
    assert hasattr(syn1, "sample")

    # CIR testing
    h1, tau1 = syn1(batch_size=3, num_time_steps=14, sampling_frequency=syn1.fft_size * syn1.subcarrier_spacing)
    h2, tau2 = syn2(batch_size=3, num_time_steps=14, sampling_frequency=syn2.fft_size * syn2.subcarrier_spacing)

    assert torch.allclose(h1, h2), "SyntheticCDLChannel impulse response must be deterministic"
    assert torch.allclose(tau1, tau2), "SyntheticCDLChannel delays must be deterministic"
    assert h1.shape == (3, 1, 2, 1, 1, 24, 14)

    # Test default sampling_frequency parameter
    h_def, tau_def = syn1(batch_size=3, num_time_steps=14)
    assert h_def.shape == (3, 1, 2, 1, 1, 24, 14)

    # Frequency response sample() testing
    syn1_s = SyntheticCDLChannel(seed=777)
    syn2_s = SyntheticCDLChannel(seed=777)
    h_freq1 = syn1_s.sample(batch_size=3)
    h_freq2 = syn2_s.sample(batch_size=3)

    assert torch.allclose(h_freq1, h_freq2), "SyntheticCDLChannel sample() must be deterministic"
    assert h_freq1.shape == (3, 2, 1, 14, 128)


def test_cdl_speed_configuration():
    """Verify CDL channel speed configuration for static (v=0.0) and mobile (v=30.0) scenarios."""
    # 1. Static channel (v=0.0)
    cdl_static = make_cdl(v=0.0)
    assert cdl_static._min_speed == 0.0
    assert cdl_static._max_speed == 0.0

    # 2. Moving channel (v=30.0)
    cdl_moving = make_cdl(v=30.0)
    assert cdl_moving._min_speed == 30.0
    assert cdl_moving._max_speed == 30.0

    # 3. Synthetic CDL channel speed contract
    cdl_syn_static = make_cdl(v=0.0, use_synthetic=True)
    assert cdl_syn_static._min_speed == 0.0
    assert cdl_syn_static._max_speed == 0.0

    cdl_syn_moving = make_cdl(v=30.0, use_synthetic=True)
    assert cdl_syn_moving._min_speed == 30.0
    assert cdl_syn_moving._max_speed == 30.0


def test_batch_generator_bit_determinism():
    """Verify bit and channel determinism with identical seeds in batch_generator."""
    b1 = batch_generator(seed=42, batch_size=2)
    b2 = batch_generator(seed=42, batch_size=2)
    assert torch.equal(b1.b, b2.b), "b tensors must be bit-exact across identical seeds"
    assert torch.allclose(b1.H, b2.H), "H tensors must match across identical seeds"
