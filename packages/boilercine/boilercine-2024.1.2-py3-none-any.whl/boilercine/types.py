"""Types relevant to CINE video processing."""

from typing import TypeAlias

import numpy as np
from numpy import typing as npt

NBit: TypeAlias = npt.NBitBase
"""A number with arbitrary precision."""

ArrFloat: TypeAlias = npt.NDArray[np.floating[NBit]]
"""An integer array with arbitrary bit depth."""

ArrDT: TypeAlias = npt.NDArray[np.datetime64]
"""Datetime array type."""

ArrInt: TypeAlias = npt.NDArray[np.integer[NBit]]
"""An integer array."""

Img: TypeAlias = ArrInt
"""An integer array representing an image."""
