#!/usr/bin/env python
"""
use Python with FFprobe to extract
JSON metadata from any kind of media file that FFprobe can read.
"""
import asyncio
import json
import subprocess
from typing import Dict, Iterable, AsyncGenerator
from pathlib import Path
import shutil

FFPROBE = shutil.which('ffprobe')
if not FFPROBE:
    raise FileNotFoundError('FFPROBE not found')


async def get_meta(files: Iterable[Path]) -> AsyncGenerator[dict, None]:  # mypy bug Dict[str, str]

    futures = [ffprobe(file) for file in files]
    for future in asyncio.as_completed(futures):
        try:
            meta = await future
        except asyncio.TimeoutError:
            continue

        yield meta


async def ffprobe(file: Path) -> Dict[str, str]:
    """ get media metadata """

    proc = await asyncio.create_subprocess_exec(*[FFPROBE, '-loglevel', 'warning',
                                                  '-print_format', 'json',
                                                  '-show_streams',
                                                  '-show_format',
                                                  str(file)],
                                                stdout=asyncio.subprocess.PIPE)

    stdout, _ = await proc.communicate()

    return json.loads(stdout.decode('utf8'))


def ffprobe_sync(file: Path) -> dict:  # mypy bug Dict[str, str]
    """ get media metadata """

    meta = subprocess.check_output([FFPROBE, '-v', 'warning',
                                    '-print_format', 'json',
                                    '-show_streams',
                                    '-show_format',
                                    str(file)],
                                   text=True)

    return json.loads(meta)
