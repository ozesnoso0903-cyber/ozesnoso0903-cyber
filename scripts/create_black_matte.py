#!/usr/bin/env python3
"""Utility to generate a 100x100 black matte image safely.

This helper mirrors the editorial guidance for ensuring the destination
folder exists before writing. It also validates the saved image to confirm
it matches the expected shape and color.
"""
from __future__ import annotations

import argparse
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
        for coord in [(0, 0), (size[0] - 1, 0), (0, size[1] - 1), (size[0] - 1, size[1] - 1), (size[0] // 2, size[1] // 2)]:
            if img.getpixel(coord) != (0, 0, 0):
                raise ValueError(f"Pixel at {coord} is not black: {img.getpixel(coord)}")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a 100x100 black matte image.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("output"),
        help="Directory where the image will be written (default: ./output)",
    )
    parser.add_argument(
        "--filename",
        default="black_matte.png",
        help="Filename for the generated image (default: black_matte.png)",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    output_path = prepare_output_path(args.output_dir / args.filename)
    image = create_black_matte()
    save_image(image, output_path)
    validate_saved_image(output_path)
    print(f"Saved black matte to {output_path}")


if __name__ == "__main__":
    main()
