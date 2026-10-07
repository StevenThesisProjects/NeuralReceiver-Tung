"""Unit tests for Doppler autocorrelation and correlation feature extraction (src/rx/features.py)."""

import math
import numpy as np
import pytest
import torch

from src.rx.features import jakes_autocorrelation, rho_hat
from src.sim.channels import make_cdl
from src.sim.link import LinkConfig, batch_generator


def test_jakes_autocorrelation_reference_values():
    """Verify theoretical Jakes autocorrelation matches standard analytical reference points."""
    # 1. v = 0.0 m/s -> rho = 1.000
    rho_0 = jakes_autocorrelation(0.0)
    assert abs(rho_0 - 1.000) < 1e-3, f"Expected 1.000 at v=0, got {rho_0}"

    # 2. v = 10.0 m/s -> rho = 0.986 (+- 0.005)
    rho_10 = jakes_autocorrelation(10.0)
    assert abs(rho_10 - 0.986) <= 0.005, f"Expected 0.986 at v=10, got {rho_10}"

    # 3. v = 40.0 m/s -> rho = 0.790 (+- 0.010)
    rho_40 = jakes_autocorrelation(40.0)
    assert abs(rho_40 - 0.790) <= 0.010, f"Expected 0.790 at v=40, got {rho_40}"

    # 4. v = 97.2 m/s -> rho = 0.062 (+- 0.010)
    rho_97_2 = jakes_autocorrelation(97.2)
    assert abs(rho_97_2 - 0.062) <= 0.010, f"Expected 0.062 at v=97.2, got {rho_97_2}"


def _simulate_isotropic_dmrs(
    v: float,
    batch_size: int = 400,
    num_subcarriers: int = 64,
    num_paths: int = 150,
    seed: int = 42,
) -> Tuple[torch.Tensor, torch.Tensor]:
    """Generate 2D isotropic Rayleigh fading pilot observations at DMRS symbols 2 and 11."""
    np.random.seed(seed)
    fd = float(v) * 3.5e9 / 3.0e8
    dt = 9.0 * (0.5e-3 / 14.0)

    theta = np.random.uniform(0, 2 * np.pi, (batch_size, 1, num_paths))
    phi = np.random.uniform(0, 2 * np.pi, (batch_size, num_subcarriers, num_paths))

    h0 = np.sum(np.exp(1j * phi), axis=-1) / np.sqrt(num_paths)
    h1 = np.sum(np.exp(1j * (2 * np.pi * fd * dt * np.cos(theta) + phi)), axis=-1) / np.sqrt(num_paths)

    H0 = torch.from_numpy(h0).to(torch.complex64).unsqueeze(1)  # [B, 1, F]
    H1 = torch.from_numpy(h1).to(torch.complex64).unsqueeze(1)  # [B, 1, F]
    return H0, H1


def test_rho_hat_vs_jakes():
    """Verify rho_hat matches theoretical Bessel J_0 within error <= 0.05 across velocities."""
    velocities = [0.0, 10.0, 40.0, 97.2]

    # Test on 2D isotropic scattering (pure Jakes model)
    for v in velocities:
        H0, H1 = _simulate_isotropic_dmrs(v, batch_size=400, num_subcarriers=64, seed=int(v * 10 + 42))
        rho_est = rho_hat((H0, H1), no=0.0, debias=False)
        mean_rho = torch.mean(rho_est).item()
        j_val = jakes_autocorrelation(v)
        err = abs(mean_rho - j_val)
        assert err <= 0.05, f"At v={v} m/s: expected |mean_rho - j_val| <= 0.05, got |{mean_rho:.4f} - {j_val:.4f}| = {err:.4f}"

    # Also verify on CDL channel model at static (0 m/s) and walking (10 m/s)
    link_cfg = LinkConfig.from_config()
    for v_cdl in [0.0, 10.0]:
        cdl = make_cdl(model="C", v=v_cdl, seed=42)
        batch = batch_generator(channel=cdl, link_config=link_cfg, batch_size=16, ebno_db=25.0, seed=42)
        H_cdl = batch.H
        rho_cdl = rho_hat(H_cdl, no=batch.N0, debias=True)
        mean_rho_cdl = torch.mean(rho_cdl).item()
        j_val_cdl = jakes_autocorrelation(v_cdl)
        err_cdl = abs(mean_rho_cdl - j_val_cdl)
        assert err_cdl <= 0.05, f"CDL v={v_cdl}: expected err <= 0.05, got {err_cdl:.4f}"


def test_rho_hat_noise_bias_correction():
    """Verify noise bias correction restores true Doppler correlation under noisy SNR."""
    np.random.seed(42)
    torch.manual_seed(42)

    num_samples = 15000
    rho_true = 0.80

    # Generate unit-power channel components with correlation rho_true
    H0_clean = (torch.randn(1, 2, num_samples) + 1j * torch.randn(1, 2, num_samples)) / np.sqrt(2.0)
    H1_clean = rho_true * H0_clean + np.sqrt(1.0 - rho_true**2) * (
        (torch.randn(1, 2, num_samples) + 1j * torch.randn(1, 2, num_samples)) / np.sqrt(2.0)
    )

    # Add AWGN with N0 = 0.1 (SNR = 10 dB)
    N0 = 0.1
    W0 = (torch.randn(1, 2, num_samples) + 1j * torch.randn(1, 2, num_samples)) * np.sqrt(N0 / 2.0)
    W1 = (torch.randn(1, 2, num_samples) + 1j * torch.randn(1, 2, num_samples)) * np.sqrt(N0 / 2.0)
    H0_noisy = H0_clean + W0
    H1_noisy = H1_clean + W1

    # Estimate with debias=False vs debias=True
    rho_biased = rho_hat((H0_noisy, H1_noisy), no=N0, debias=False).item()
    rho_debiased = rho_hat((H0_noisy, H1_noisy), no=N0, debias=True).item()

    err_biased = abs(rho_biased - rho_true)
    err_debiased = abs(rho_debiased - rho_true)

    # Debiased estimate must be significantly closer to true correlation than biased estimate
    assert err_debiased < err_biased, (
        f"Expected debiased error ({err_debiased:.4f}) < biased error ({err_biased:.4f})"
    )
    assert err_debiased < 0.02, f"Debiased error must be < 0.02, got {err_debiased:.4f}"


def test_rho_hat_shapes_and_invariance():
    """Verify rho_hat handles 4D, 5D, 7D, 2-pilot tensor, and tuple inputs invariantly."""
    batch_size = 4
    num_rx = 2
    num_symbols = 14
    fft_size = 128
    effective_sc = 116

    # 1. 4D: [B, rx_ant, T, F]
    H_4d = torch.randn(batch_size, num_rx, num_symbols, fft_size, dtype=torch.complex64)
    res_4d = rho_hat(H_4d, no=0.01)
    assert res_4d.shape == (batch_size,)
    assert torch.all(torch.isfinite(res_4d))
    assert torch.all(res_4d >= -1.0) and torch.all(res_4d <= 1.0)

    # 2. 5D: [B, 1, rx_ant, T, F]
    H_5d_a = H_4d.unsqueeze(1)
    res_5d_a = rho_hat(H_5d_a, no=0.01)
    assert torch.allclose(res_4d, res_5d_a, atol=1e-6)

    # 3. 5D: [B, rx_ant, 1, T, F]
    H_5d_b = H_4d.unsqueeze(2)
    res_5d_b = rho_hat(H_5d_b, no=0.01)
    assert torch.allclose(res_4d, res_5d_b, atol=1e-6)

    # 4. 7D: [B, 1, rx_ant, 1, 1, T, F_eff]
    H_7d = torch.randn(batch_size, 1, num_rx, 1, 1, num_symbols, effective_sc, dtype=torch.complex64)
    res_7d = rho_hat(H_7d, no=0.01)
    assert res_7d.shape == (batch_size,)
    assert torch.all(torch.isfinite(res_7d))
    assert torch.all(res_7d >= -1.0) and torch.all(res_7d <= 1.0)

    # 5. 2-pilot tensor: [2, B, rx_ant, F]
    H_2pilot = torch.stack([H_4d[:, :, 2, :], H_4d[:, :, 11, :]], dim=0)
    res_2pilot = rho_hat(H_2pilot, no=0.01)
    assert torch.allclose(res_4d, res_2pilot, atol=1e-6)

    # 6. Tuple: (H0, H1)
    res_tuple = rho_hat((H_4d[:, :, 2, :], H_4d[:, :, 11, :]), no=0.01)
    assert torch.allclose(res_4d, res_tuple, atol=1e-6)


def test_rho_hat_with_b0_receiver():
    """Verify rho_hat extracts Doppler correlation reliably from b0_receiver channel estimates."""
    link_config = LinkConfig.from_config()
    batch = batch_generator(link_config=link_config, batch_size=4, ebno_db=20.0, seed=42)
    b, Y, X_pilot, N0, H = batch

    from src.rx.classical import b0_receiver

    llr, h_hat = b0_receiver(Y, N0, link_config=link_config)

    rho_vals = rho_hat(h_hat, no=N0, debias=True)
    assert rho_vals.shape == (4,)
    assert torch.all(torch.isfinite(rho_vals))

    # At speed = 0.0 m/s (static link), rho should be very close to 1.0
    assert torch.all(rho_vals > 0.98), f"Expected rho > 0.98 for static link, got {rho_vals}"
