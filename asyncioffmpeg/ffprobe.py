#!/usr/bin/env python
import asyncio
import json
from pathlib import Path
import shutil
import sys
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


async def main(filein: Path) -> float:
    try:
        meta = await asyncio.wait_for(ffprobe(filein), timeout=0.5)
        duration = float(meta['streams'][0]['duration'])
        return duration
    except asyncio.TimeoutError:
        print('timeout ', filein, file=sys.stderr)
