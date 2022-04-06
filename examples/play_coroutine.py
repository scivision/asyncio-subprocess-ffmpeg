#!/usr/bin/env python3
from argparse import ArgumentParser
import asyncio

import asyncioffmpeg.ffplay as play
from asyncioffmpeg import get_videos


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

asyncio.run(play.main(flist))
