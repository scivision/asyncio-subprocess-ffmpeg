#!/usr/bin/env python3
"""
ProcessPoolExecutor would work similarly,
but is not needed here since all computation is done in the external program.
"""

from pathlib import Path
import subprocess
from argparse import ArgumentParser
import concurrent.futures
import shutil

from asyncioffmpeg import get_videos

EXE = shutil.which("ffplay")
if not EXE:
    raise FileNotFoundError("ffplay")


def ffplay(filein: Path):
    subprocess.check_call([EXE, "-v", "warning", "-autoexit", str(filein)])


if __name__ == "__main__":
    p = ArgumentParser(description="Asynchronous playback with ThreadPool and FFplay")
    p.add_argument("path", help="directory where media files are kept")
    p.add_argument(
        "-suffix",
        help="file suffixes of desired media file types",
        nargs="+",
    )
    P = p.parse_args()

    flist = get_videos(P.path, P.suffix)
    print("found", len(flist), "files in", P.path)

    with concurrent.futures.ThreadPoolExecutor(max_workers=2, thread_name_prefix="ffplay") as pool:
        pool.map(ffplay, flist)
