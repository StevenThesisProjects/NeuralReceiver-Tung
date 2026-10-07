"""Simulation and channel modeling package for nrx-bounded pipeline."""

from src.sim.channels import SyntheticCDL, SyntheticCDLChannel, make_cdl
from src.sim.link import BatchData, LinkConfig, batch_generator

__all__ = [
    "make_cdl",
    "SyntheticCDL",
    "SyntheticCDLChannel",
    "LinkConfig",
    "batch_generator",
    "BatchData",
]
