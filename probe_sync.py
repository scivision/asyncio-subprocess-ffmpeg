#!/usr/bin/env python
import time
from pathlib import Path
from argparse import ArgumentParser
import asyncioffmpeg.ffprobe as probe


if __name__ == "__main__":
    p = ArgumentParser(description="Get media metadata synchronously with FFprobe")
    p.add_argument("path", help="directory where media files are kept")
    p.add_argument(
        "-suffix",
        help="file suffixes of desired media file types",
        nargs="+",
        default=[".mp3", ".mp4", ".avi", ".ogv", ".ogg"],
    )
    P = p.parse_args()

    tic = time.monotonic()
    path = Path(P.path).expanduser()
    if not path.is_dir():
        raise FileNotFoundError(f"{path} is not a directory")

    flist = (f for f in path.iterdir() if f.is_file() and f.suffix in P.suffix)

    for f in flist:
        meta = probe.ffprobe_sync(f)
        probe.print_meta(meta)

    print("ffprobe sync: {:.3f} seconds".format(time.monotonic() - tic))
