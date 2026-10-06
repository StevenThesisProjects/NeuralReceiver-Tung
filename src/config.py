"""Configuration loader module for nrx-bounded.

Provides unified access to config/config.yaml single-source parameters.
"""

import os
from pathlib import Path
from typing import Any, Dict
import yaml


def get_default_config_path() -> Path:
    """Find default config/config.yaml relative to project root or current working dir."""
    current_file = Path(__file__).resolve()
    # If in src/config.py, project root is parent directory
    project_root = current_file.parent.parent
    candidate = project_root / "config" / "config.yaml"
    if candidate.exists():
        return candidate
    # Fallback to current working directory
    fallback = Path.cwd() / "config" / "config.yaml"
    if fallback.exists():
        return fallback
    return candidate


def load_config(path: str = None) -> Dict[str, Any]:
    """Load and parse the project YAML configuration.

    Parameters
    ----------
    path : str, optional
        Path to config.yaml. If None, resolves to default location.

    Returns
    -------
    dict
        Parsed configuration dictionary.
    """
    config_file = Path(path) if path else get_default_config_path()
    if not config_file.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_file}")

    with open(config_file, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    return config


if __name__ == "__main__":
    cfg = load_config()
    print("SUCCESS: Successfully loaded configuration!")
    print(f"  Seed: {cfg.get('seed')}")
    print(f"  PHY Modulation: {cfg.get('phy', {}).get('modulation', {}).get('type')}")
    print(f"  FFT Size: {cfg.get('phy', {}).get('fft_size')}")
    print(f"  Proposed Model Layers: {cfg.get('models', {}).get('proposed_axial', {}).get('num_layers')}")
    print(f"  In Channels: {cfg.get('models', {}).get('proposed_axial', {}).get('in_channels')}")
