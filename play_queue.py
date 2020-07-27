#!/usr/bin/env python3
"""
example of using queue with non-asyncio subprocess and threading
"""

from argparse import ArgumentParser
import queue
import threading

import asyncioffmpeg.ffplay as play
from asyncioffmpeg import get_videos

NTHREADS = 2


if __name__ == "__main__":
    p = ArgumentParser(description="Plays media files with FFplay")
    p.add_argument("path", help="directory where media files are kept")
    p.add_argument(
        "-suffix", help="file suffixes of desired media file types", nargs="+",
    )
    P = p.parse_args()

    flist = get_videos(P.path, P.suffix)
    print("found", len(flist), "files in", P.path)

    qin = queue.Queue()  # type: ignore
    for fn in flist:
        qin.put(fn)

    threads = []
    for _ in range(NTHREADS):
        t = threading.Thread(target=play.ffplay_sync, args=(qin,))
        t.start()
        threads.append(t)

    # In general one would use the following lines to block until the tasks are done.
    qin.join()
    for t in threads:
        t.join()
