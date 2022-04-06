from pathlib import Path
import typing as T
import os
import asyncio

if os.name == "nt":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())  # type: ignore


def get_videos(path: Path, suffixes: T.Sequence[str] = None) -> T.List[Path]:

    if not suffixes:
        suffixes = [".mp4", ".avi", ".ogv", ".wmv", ".flv", ".mov"]

    path = Path(path).expanduser()

    if not path.is_dir():
        raise FileNotFoundError(f"{path} is not a directory")

    flist = [f for f in path.iterdir() if f.is_file() and f.suffix in suffixes]
    if len(flist) == 0:
        raise FileNotFoundError(f"No files found in {path} with {suffixes}")
    return flist
