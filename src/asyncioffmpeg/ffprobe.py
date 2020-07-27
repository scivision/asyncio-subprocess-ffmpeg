"""
use Python with FFprobe to extract
JSON metadata from any kind of media file that FFprobe can read.
"""

import asyncio
import json
import subprocess
import typing
from pathlib import Path
import shutil

from . import get_videos

FFPROBE = shutil.which("ffprobe")
if not FFPROBE:
    raise ImportError("FFPROBE not found")


def print_meta(meta: typing.Dict[str, typing.Any]):
    fn = Path(meta["format"]["filename"])
    dur = float(meta["streams"][0]["duration"])
    print("{:>40}  {:>5.1f}".format(fn.name, dur))


async def get_meta_gather(path: Path, suffix: str) -> typing.List[typing.Dict[str, typing.Any]]:
    """ for comparison with asyncio.as_completed"""
    futures = [ffprobe(f) for f in get_videos(path, suffix)]
    metas = await asyncio.gather(*futures)
    for meta in metas:
        print_meta(meta)

    return metas


async def get_meta(path: Path, suffix: str) -> typing.List[typing.Dict[str, typing.Any]]:
    futures = [ffprobe(f) for f in get_videos(path, suffix)]
    metas = []
    for file in asyncio.as_completed(futures):
        meta = await file
        print_meta(meta)
        metas.append(meta)

    return metas


async def ffprobe(file: Path) -> typing.Dict[str, typing.Any]:
    """ get media metadata """
    proc = await asyncio.create_subprocess_exec(
        *[
            FFPROBE,
            "-loglevel",
            "warning",
            "-print_format",
            "json",
            "-show_streams",
            "-show_format",
            str(file),
        ],
        stdout=asyncio.subprocess.PIPE
    )

    stdout, _ = await proc.communicate()

    return json.loads(stdout.decode("utf8"))


def ffprobe_sync(file: Path) -> typing.Dict[str, typing.Any]:
    """ get media metadata """
    meta = subprocess.check_output(
        [
            FFPROBE,
            "-v",
            "warning",
            "-print_format",
            "json",
            "-show_streams",
            "-show_format",
            str(file),
        ],
        text=True,
    )

    return json.loads(meta)
