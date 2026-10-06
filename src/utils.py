"""Utility functions for nrx-bounded."""

import os
import random
import numpy as np
import torch


def set_all_seeds(seed: int = 42) -> None:
    """Set random seed for reproducibility across Python, NumPy, PyTorch, and TensorFlow.

    Parameters
    ----------
    seed : int, default=42
        Integer seed value to set across all RNGs.
    """
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
    try:
        import tensorflow as tf
        tf.random.set_seed(seed)
    except ImportError:
        pass


if __name__ == "__main__":
    print("Testing reproducibility with set_all_seeds(42)...")
    
    # Run 1
    set_all_seeds(42)
    py_rand_1 = random.random()
    np_rand_1 = np.random.randn(5)
    torch_rand_1 = torch.randn(5)

    # Run 2
    set_all_seeds(42)
    py_rand_2 = random.random()
    np_rand_2 = np.random.randn(5)
    torch_rand_2 = torch.randn(5)

    assert py_rand_1 == py_rand_2, "Python random seed failure!"
    assert np.allclose(np_rand_1, np_rand_2), "NumPy random seed failure!"
    assert torch.allclose(torch_rand_1, torch_rand_2), "PyTorch random seed failure!"

    print("SUCCESS: All random number generators are 100% deterministic and reproducible!")
