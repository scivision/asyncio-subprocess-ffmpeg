"""
synchronous FFprobe
"""

from pathlib import Path
import subprocess
import shutil
import json

FFPROBE = shutil.which('ffprobe')
if not FFPROBE:
    raise FileNotFoundError('FFPROBE not found')

TIMEOUT = 5.0  # 2.0 is too short for Windows


def ffprobe_sync(filein: Path) -> dict:
    """ get media metadata """
    assert isinstance(FFPROBE, str)

    meta = subprocess.check_output([FFPROBE, '-v', 'warning',
                                    '-print_format', 'json',
                                    '-show_streams',
                                    '-show_format',
                                    str(filein)],
                                   text=True, timeout=TIMEOUT)

    return json.loads(meta)
