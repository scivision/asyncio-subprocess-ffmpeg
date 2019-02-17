#!/usr/bin/env python
import asyncio
import json
from pathlib import Path
import shutil
import sys
from argparse import ArgumentParser
import subprocess

if sys.version_info < (3, 7):
    raise RuntimeError('Python >= 3.7 required')


FFPROBE = shutil.which('ffprobe')
if not FFPROBE:
    raise FileNotFoundError('FFPROBE not found')


async def ffprobe(filein: Path):
    """ get media metadata """
    assert isinstance(FFPROBE, str)

    proc = await asyncio.create_subprocess_exec(*[FFPROBE, '-v', 'warning',
                                                  '-print_format', 'json',
                                                  '-show_streams',
                                                  '-show_format', str(filein)],
                                                stdout=subprocess.PIPE,
                                                stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    return json.loads(stdout.decode('utf8'))


async def main(filein: Path):
    try:
        meta = await asyncio.wait_for(ffprobe(filein), timeout=0.5)
        duration = float(meta['streams'][0]['duration'])
        print(f"{filein.name:>40}  {duration:>5.1f}")
    except asyncio.TimeoutError:
        print('timeout ', filein, file=sys.stderr)


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

    flist = (f for f in path.iterdir() if f.is_file() and f.suffix in P.suffix)

    futures = [main(f) for f in flist]

    asyncio.run(asyncio.wait(futures))
