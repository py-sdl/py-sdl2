"""Examples for PySDL2.

This package contains the examples for sdl2.
"""
import os
from sdl2.ext import Resources

__all__ = ["RESOURCES"]

_fpath = os.path.dirname(os.path.abspath(__file__))
RESOURCES = Resources(os.path.join(_fpath, "resources"))
