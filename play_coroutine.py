#!/usr/bin/env python
from pathlib import Path
from argparse import ArgumentParser

import asyncioffmpeg.ffplay as play
from asyncioffmpeg.runner import runner


if __name__ == "__main__":
    p = ArgumentParser(description="Plays media files asynchronously with FFplay")
    p.add_argument("path", help="directory where media files are kept")
    p.add_argument(
        "-suffix",
        help="file suffixes of desired media file types",
        nargs="+",
        default=[".mp4", ".avi", ".ogv", ".wmv", ".flv", ".mov", ".ogg"],
    )
    P = p.parse_args()

    path = Path(P.path).expanduser()
    if not path.is_dir():
        raise NotADirectoryError(path)

    flist = (f for f in path.iterdir() if f.is_file() and f.suffix in P.suffix)

    runner(play.main, flist)
