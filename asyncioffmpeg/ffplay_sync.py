"""
example of non-async queue
"""
import queue
import subprocess
import shutil
import sys

FFPLAY = shutil.which('ffplay')
if not FFPLAY:
    raise FileNotFoundError('FFPLAY not found')


def ffplay_sync(qin: queue.Queue):
    """
    Play media.
    """

    while not qin.empty():
        filein = qin.get(timeout=1.0)

        cmd = [FFPLAY, '-v', 'warning', '-autoexit', str(filein)]

        ret = subprocess.run(cmd)

        if ret.returncode != 0:
            print(filein, 'playback failure', cmd, file=sys.stderr)

        qin.task_done()
