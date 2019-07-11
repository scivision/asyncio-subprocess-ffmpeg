#!/usr/bin/env python
"""
example of using queue with non-asyncio subprocess and threading
"""
from pathlib import Path
from argparse import ArgumentParser
import queue
import threading

import asyncioffmpeg.ffplay as play

NTHREADS = 2


if __name__ == "__main__":
    p = ArgumentParser(description="Plays media files with FFplay")
    p.add_argument("path", help="directory where media files are kept")
    p.add_argument(
        "-suffix",
        help="file suffixes of desired media file types",
        nargs="+",
        default=[".mp4", ".avi", ".ogv", ".wmv", ".flv", ".mov"],
    )
    P = p.parse_args()

    path = Path(P.path).expanduser()

    flist = (f for f in path.iterdir() if f.is_file() and f.suffix in P.suffix)

    qin = queue.Queue()  # type: ignore
    for fn in flist:
        qin.put(fn)

    threads = []
    for i in range(NTHREADS):
        t = threading.Thread(target=play.ffplay_sync, args=(qin,))
        t.start()
        threads.append(t)

    # In general one would use the following lines to block until the tasks are done.
    qin.join()
    for t in threads:
        t.join()
