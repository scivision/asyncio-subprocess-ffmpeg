#!/usr/bin/env python
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


def ffprobe(filein: Path):
    """ get media metadata """
    assert isinstance(FFPROBE, str)

    stdout = subprocess.check_output([FFPROBE, '-v', 'warning',
                                      '-print_format', 'json',
                                      '-show_streams',
                                      '-show_format', str(filein)],
                                     text=True,
                                     timeout=1.)

    return json.loads(stdout)


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
        meta = ffprobe(f)
        duration = float(meta['streams'][0]['duration'])
        print(f"{f.name:>40}  {duration:>5.1f}")
