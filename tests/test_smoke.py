"""Smoke test suite for nrx-bounded infrastructure."""

import numpy as np
import torch
import yaml

from src import load_config, set_all_seeds
import src.config
import src.utils


def test_imports():
    """Verify that all core project modules and libraries import cleanly."""
    assert src is not None
    assert src.config is not None
    assert src.utils is not None
    assert torch is not None
    assert np is not None
    assert yaml is not None


def test_config_validity():
    """Verify single-source config/config.yaml integrity and key PHY/model parameters."""
    cfg = load_config()
    assert isinstance(cfg, dict), "Config should load as a dictionary"
    assert cfg.get("seed") == 42, f"Expected seed=42, got {cfg.get('seed')}"

    phy = cfg.get("phy", {})
    assert phy.get("fft_size") == 128, f"Expected fft_size=128, got {phy.get('fft_size')}"
    assert phy.get("num_ofdm_symbols") == 14, f"Expected num_ofdm_symbols=14, got {phy.get('num_ofdm_symbols')}"

    models = cfg.get("models", {})
    axial = models.get("proposed_axial", {})
    assert axial.get("d_model") == 128, f"Expected d_model=128, got {axial.get('d_model')}"
    assert axial.get("num_layers") == 6, f"Expected num_layers=6, got {axial.get('num_layers')}"
    assert axial.get("in_channels") == 12, f"Expected in_channels=12, got {axial.get('in_channels')}"


def test_seed_reproducibility():
    """Verify deterministic RNG behavior across NumPy and PyTorch."""
    # Run 1
    set_all_seeds(1234)
    np_sample_1 = np.random.randn(10, 10)
    torch_sample_1 = torch.randn(10, 10)

    # Run 2
    set_all_seeds(1234)
    np_sample_2 = np.random.randn(10, 10)
    torch_sample_2 = torch.randn(10, 10)

    assert np.allclose(np_sample_1, np_sample_2), "NumPy RNG must be deterministic"
    assert torch.allclose(torch_sample_1, torch_sample_2), "PyTorch RNG must be deterministic"
