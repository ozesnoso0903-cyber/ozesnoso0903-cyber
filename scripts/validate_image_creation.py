"""Utilities to safely create and validate small placeholder images.

This module mirrors the editorial guidance to ensure the destination
directory exists before writing files and to reopen the saved artifact to
confirm it matches the expected shape and pixel data.
"""
from __future__ import annotations

from pathlib import Path
from typing import Tuple

from PIL import Image

DEFAULT_SIZE: Tuple[int, int] = (100, 100)
DEFAULT_COLOR = "black"


def prepare_output_path(path: Path) -> Path:
    """Ensure the parent directory exists for the output image."""

    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def create_black_matte(size: Tuple[int, int] = DEFAULT_SIZE) -> Image.Image:
    """Create an RGB image filled with black pixels."""

    return Image.new("RGB", size, color=DEFAULT_COLOR)


def save_image(image: Image.Image, destination: Path) -> Path:
    """Save the image to disk."""

    image.save(destination)
    return destination


def validate_saved_image(path: Path, size: Tuple[int, int] = DEFAULT_SIZE) -> None:
    """Open the saved image to verify size, mode, and pixel content."""

    with Image.open(path) as img:
        img.load()
        if img.size != size:
            raise ValueError(f"Unexpected image size: {img.size}; expected {size}")
        if img.mode != "RGB":
            raise ValueError(f"Unexpected mode: {img.mode}; expected RGB")

        # Spot-check a few pixels to ensure the matte is uniformly black.
        corners_and_center = [
            (0, 0),
            (size[0] - 1, 0),
            (0, size[1] - 1),
            (size[0] - 1, size[1] - 1),
            (size[0] // 2, size[1] // 2),
        ]
        for coord in corners_and_center:
            if img.getpixel(coord) != (0, 0, 0):
                raise ValueError(f"Pixel at {coord} is not black: {img.getpixel(coord)}")

