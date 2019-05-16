#!/usr/bin/env python
from pathlib import Path
import shutil
from argparse import ArgumentParser
import asyncioffmpeg.ffprobe_sync as probe

FFPROBE = shutil.which('ffprobe')
if not FFPROBE:
    raise FileNotFoundError('FFPROBE not found')


if __name__ == '__main__':
    p = ArgumentParser(
        description="Get media metadata synchronously with FFprobe")
    p.add_argument('path', help='directory where media files are kept')
    p.add_argument('-suffix', help='file suffixes of desired media file types',
                   nargs='+', default=['.mp4', '.avi', '.ogv'])
    P = p.parse_args()

    path = Path(P.path).expanduser()
    if not path.is_dir():
        raise FileNotFoundError(f'{path} is not a directory')

    flist = (f for f in path.iterdir() if f.is_file() and f.suffix in P.suffix)

    for f in flist:
        meta = probe.ffprobe_sync(f)
        duration = float(meta['streams'][0]['duration'])
        print(f"{f.name:>40}  {duration:>5.1f}")
