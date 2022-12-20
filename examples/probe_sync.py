#!/usr/bin/env python3
import time
from argparse import ArgumentParser

import asyncioffmpeg.ffprobe as probe
from asyncioffmpeg import get_videos


p = ArgumentParser(description="Get media metadata synchronously with FFprobe")
p.add_argument("path", help="directory where media files are kept")
p.add_argument(
    "-suffix",
    help="file suffixes of desired media file types",
    nargs="+",
)
P = p.parse_args()

tic = time.monotonic()
for f in get_videos(P.path, set(P.suffix)):
    meta = probe.ffprobe_sync(f)
    probe.print_meta(meta)

print(f"ffprobe sync: {time.monotonic() - tic:.3f} seconds")
