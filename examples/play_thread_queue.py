#!/usr/bin/env python3
from argparse import ArgumentParser
import concurrent.futures
import queue
from pathlib import Path
import shutil
import subprocess

from asyncioffmpeg import get_videos

EXE = shutil.which("ffplay")
if not EXE:
    raise FileNotFoundError("ffplay")


def ffplay(filein: Path):
    subprocess.check_call([EXE, "-v", "warning", "-autoexit", str(filein)])


def main(qin: queue.Queue):
    with concurrent.futures.ThreadPoolExecutor(max_workers=2, thread_name_prefix="ffplay") as pool:
        while not qin.empty():
            pool.submit(ffplay, qin.get(timeout=1.0))
            qin.task_done()


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

    qin = queue.Queue()  # type: ignore
    for fn in flist:
        qin.put(fn)

    main(qin)
    qin.join()
