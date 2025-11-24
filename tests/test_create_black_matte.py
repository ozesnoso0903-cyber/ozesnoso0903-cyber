from __future__ import annotations

from pathlib import Path

import pytest

pytest.importorskip("PIL")
from PIL import Image

from scripts.validate_image_creation import (
    create_black_matte,
    prepare_output_path,
    save_image,
    validate_saved_image,
)


def test_prepare_output_path_creates_parent(tmp_path: Path) -> None:
    target = tmp_path / "output" / "black_matte.png"
    prepared = prepare_output_path(target)

    assert prepared == target
    assert target.parent.exists()
    assert target.parent.is_dir()


def test_save_and_validate_generates_black_image(tmp_path: Path) -> None:
    destination = prepare_output_path(tmp_path / "output" / "black_matte.png")
    image = create_black_matte()

    save_image(image, destination)
    validate_saved_image(destination)

    with Image.open(destination) as saved:
        saved.load()
        assert saved.size == (100, 100)
        assert saved.mode == "RGB"
        assert saved.getpixel((50, 50)) == (0, 0, 0)


@pytest.mark.parametrize("filename", ["black_matte.png", "nested/black_matte.png"])
def test_prepare_output_path_handles_nested_dirs(tmp_path: Path, filename: str) -> None:
    target = tmp_path / filename
    prepared = prepare_output_path(target)

    assert prepared == target
    assert prepared.parent.exists()
