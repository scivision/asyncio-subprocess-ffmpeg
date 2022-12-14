from __future__ import annotations
from pathlib import Path
import typing as T


def get_videos(path: Path, suffixes: str | list[str] = None) -> T.Iterator[Path]:

    if not suffixes:
        suffixes = [".mp4", ".avi", ".ogv", ".wmv", ".flv", ".mov"]
    if isinstance(suffixes, str):
        suffixes = [suffixes]

    path = Path(path).expanduser()

    if not path.is_dir():
        raise FileNotFoundError(f"{path} is not a directory")

    return (f for f in path.iterdir() if f.is_file() and f.suffix in suffixes)
