#!/usr/bin/env python
import asyncio
import os
from pathlib import Path
from argparse import ArgumentParser

import asyncioffmpeg.ffplay as play


if __name__ == '__main__':
    p = ArgumentParser(
        description="Plays media files asynchronously with FFplay")
    p.add_argument('path', help='directory where media files are kept')
    p.add_argument('-suffix', help='file suffixes of desired media file types',
                   nargs='+', default=['.mp4', '.avi', '.ogv', '.wmv', '.flv', '.mov'])
    P = p.parse_args()

    path = Path(P.path).expanduser()

    flist = (f for f in path.iterdir() if f.is_file() and f.suffix in P.suffix)

    if os.name == 'nt':
        loop = asyncio.ProactorEventLoop()  # type: ignore
        loop.run_until_complete(play.main(flist))
    else:
        asyncio.run(play.main(flist))
