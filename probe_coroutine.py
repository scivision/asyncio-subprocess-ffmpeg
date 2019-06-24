#!/usr/bin/env python
from argparse import ArgumentParser
from pathlib import Path
from typing import Sequence
import asyncio
import sys
import os

import asyncioffmpeg.ffprobe as probe


async def main(path: Path, suffix: Sequence[str]):

    path = Path(path).expanduser()
    if not path.is_dir():
        raise NotADirectoryError(path)

    files = (f for f in path.iterdir() if f.is_file() and f.suffix in suffix)

    async for meta in probe.get_meta(files):
        if not meta:
            continue
        fn = meta['format']['filename']
        dur = float(meta['streams'][0]['duration'])
        print(f"{fn:>40}  {dur:>5.1f}")


if __name__ == '__main__':
    p = ArgumentParser(
        description="Get media metadata asynchronously with FFprobe")
    p.add_argument('path', help='directory where media files are kept')
    p.add_argument('-suffix', help='file suffixes of desired media file types',
                   nargs='+', default=['.mp4', '.avi', '.ogv', '.ogg'])
    P = p.parse_args()

    if os.name == 'nt' and sys.version_info < (3, 8):
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())  # type: ignore

    asyncio.run(main(P.path, P.suffix))
