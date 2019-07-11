#!/usr/bin/env python
"""
3x to 4x speedup over ffprobe_sync on Linux
10% speedup on Windows over ffprobe_sync, even with virus monitor disabled.
"""
import time
from argparse import ArgumentParser

import asyncioffmpeg.ffprobe as probe
from asyncioffmpeg.runner import runner


if __name__ == "__main__":
    p = ArgumentParser(description="Get media metadata asynchronously with FFprobe")
    p.add_argument("path", help="directory where media files are kept")
    p.add_argument(
        "-suffix",
        help="file suffixes of desired media file types",
        nargs="+",
        default=[".mp3", ".mp4", ".avi", ".ogv", ".ogg"],
    )
    P = p.parse_args()

    tic = time.monotonic()
    # emits results as each future is completed
    runner(probe.get_meta, P.path, P.suffix)
    print("ffprobe asyncio.as_completed: {:.3f} seconds".format(time.monotonic() - tic))

    # approximately same wallclock time, but only gives results when all futures complete
    tic = time.monotonic()
    runner(probe.get_meta_gather, P.path, P.suffix)
    print("ffprobe asyncio.gather: {:.3f} seconds".format(time.monotonic() - tic))
