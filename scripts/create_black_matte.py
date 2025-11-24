#!/usr/bin/env python3
"""Utility to generate a 100x100 black matte image safely.

This helper mirrors the editorial guidance for ensuring the destination
folder exists before writing. It also validates the saved image to confirm
it matches the expected shape and color.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from validate_image_creation import (  # noqa: E402
    DEFAULT_COLOR,
    DEFAULT_SIZE,
    create_black_matte,
    prepare_output_path,
    save_image,
    validate_saved_image,
)


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
