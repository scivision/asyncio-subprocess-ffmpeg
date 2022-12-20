#!/usr/bin/env python3
"""
ProcessPoolExecutor would work similarly,
but is not needed here since all computation is done in the external program.
"""

from pathlib import Path
import subprocess
from argparse import ArgumentParser
import concurrent.futures

from asyncioffmpeg import get_videos, get_ffplay


def ffplay(filein: Path):
    subprocess.check_call([get_ffplay(), "-v", "warning", "-autoexit", str(filein)])


if __name__ == "__main__":
    p = ArgumentParser(description="Asynchronous playback with ThreadPool and FFplay")
    p.add_argument("path", help="directory where media files are kept")
    p.add_argument(
        "-suffix",
        help="file suffixes of desired media file types",
        nargs="+",
    )
    P = p.parse_args()

    flist = get_videos(P.path, set(P.suffix))

    with concurrent.futures.ThreadPoolExecutor(max_workers=2, thread_name_prefix="ffplay") as pool:
        pool.map(ffplay, flist)
