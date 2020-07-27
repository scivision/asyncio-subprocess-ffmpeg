#!/usr/bin/env python
from pathlib import Path
import subprocess
from argparse import ArgumentParser
import concurrent.futures
from asyncioffmpeg.ffplay import FFPLAY


def ffplay(filein: Path):
    assert filein.is_file()

    cmd = [FFPLAY, "-v", "warning", "-autoexit", str(filein)]

    subprocess.check_call(cmd)


if __name__ == "__main__":
    p = ArgumentParser(description="Asynchronous playback with ThreadPool and FFplay")
    p.add_argument("path", help="directory where media files are kept")
    p.add_argument(
        "-suffix",
        help="file suffixes of desired media file types",
        nargs="+",
        default=[".mp4", ".avi", ".ogv", ".wmv", ".flv", ".mov"],
    )
    P = p.parse_args()

    path = Path(P.path).expanduser()
    if not path.is_dir():
        raise FileNotFoundError(f"{path} is not a directory")

    flist = (f for f in path.iterdir() if f.is_file() and f.suffix in P.suffix)

    with concurrent.futures.ThreadPoolExecutor(max_workers=2, thread_name_prefix="ffplay") as pool:
        pool.map(ffplay, flist)
