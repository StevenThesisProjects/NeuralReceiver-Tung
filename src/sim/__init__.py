"""Simulation and channel modeling package for nrx-bounded pipeline."""

from src.sim.channels import SyntheticCDL, make_cdl
from src.sim.link import BatchData, LinkConfig, batch_generator

__all__ = [
    "make_cdl",
    "SyntheticCDL",
    "LinkConfig",
    "batch_generator",
    "BatchData",
]
