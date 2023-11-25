from __future__ import annotations

from functools import lru_cache
from pathlib import Path

_DEFAULT_CAMERA_PATH = Path("images/cameras")


@lru_cache
def get_camera_name(file: str) -> str:
    return file.split(".")[0]
