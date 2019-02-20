#!/usr/bin/env python
"""
This file contains connections from Python to FFprobe, useful for extracting
JSON metadata from any kind of media file that FFprobe can read.

Moreover, this file demonstrates asynchronous and synchronous access to
thread-safe subprocesses
"""
import asyncio
import json
from pathlib import Path
import shutil
import sys
import subprocess


FFPROBE = shutil.which('ffprobe')
if not FFPROBE:
    raise FileNotFoundError('FFPROBE not found')


# %% Asynchronous FFprobe
async def ffprobe(filein: Path) -> dict:
    """ get media metadata """
    assert isinstance(FFPROBE, str)

    proc = await asyncio.create_subprocess_exec(*[FFPROBE, '-v', 'warning',
                                                  '-print_format', 'json',
                                                  '-show_streams',
                                                  '-show_format',
                                                  str(filein)],
                                                stdout=asyncio.subprocess.PIPE,
                                                stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    return json.loads(stdout.decode('utf8'))


async def get_meta(filein: Path) -> dict:
    try:
        meta = await asyncio.wait_for(ffprobe(filein), timeout=0.5)
        return meta
    except asyncio.TimeoutError:
        print('timeout ', filein, file=sys.stderr)
        return {}

# %% synchronous FFprobe


def ffprobe_sync(filein: Path) -> dict:
    """ get media metadata """
    assert isinstance(FFPROBE, str)

    meta = subprocess.check_output([FFPROBE, '-v', 'warning',
                                    '-print_format', 'json',
                                    '-show_streams',
                                    '-show_format',
                                    str(filein)],
                                   text=True)

    return json.loads(meta)
