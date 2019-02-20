#!/usr/bin/env python
from argparse import ArgumentParser
from pathlib import Path
from typing import List
import asyncio
import asyncioffmpeg.ffprobe as probe


async def main(path: Path, suffix: List[str]):

    flist = (f for f in path.iterdir() if f.is_file() and f.suffix in suffix)

    futures = [probe.get_meta(f) for f in flist]

    metas = await asyncio.gather(*futures)

    for meta in metas:
        fn = meta['format']['filename']
        dur = float(meta['streams'][0]['duration'])
        print(f"{fn:>40}  {dur:>5.1f}")


if __name__ == '__main__':
    p = ArgumentParser(
        description="Get media metadata asynchronously with FFprobe")
    p.add_argument('path', help='directory where media files are kept')
    p.add_argument('-suffix', help='file suffixes of desired media file types',
                   nargs='+', default=['.mp4', '.avi', '.ogv'])
    P = p.parse_args()

    path = Path(P.path).expanduser()
    if not path.is_dir():
        raise FileNotFoundError(f'{path} is not a directory')

    asyncio.run(main(path, P.suffix))
