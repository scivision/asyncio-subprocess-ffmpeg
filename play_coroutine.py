#!/usr/bin/env python3
from argparse import ArgumentParser

import asyncioffmpeg.ffplay as play
from asyncioffmpeg.runner import runner
from asyncioffmpeg import get_videos


if __name__ == "__main__":
    p = ArgumentParser(description="Plays media files asynchronously with FFplay")
    p.add_argument("path", help="directory where media files are kept")
    p.add_argument(
        "-suffix",
        help="file suffixes of desired media file types",
        nargs="+",
    )
    P = p.parse_args()

    flist = get_videos(P.path, P.suffix)
    print("found", len(flist), "files in", P.path)

    runner(play.main, flist)
