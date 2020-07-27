"""
This example uses a finite number of workers, rather than slamming the system with endless subprocesses.
This is more effective than endless context switching for an overloaded CPU.
"""

import queue
import subprocess
import asyncio
from pathlib import Path
import shutil
import sys
from typing import Iterable
import os

FFPLAY = shutil.which("ffplay")
if not FFPLAY:
    raise ImportError("FFPLAY not found")


async def ffplay(queue: asyncio.Queue):
    """
    Play media asynchronously.
    Each task runs endlessly until .cancel()
    """
    assert isinstance(FFPLAY, str)

    while True:
        filein = await queue.get()

        cmd = [FFPLAY, "-loglevel", "warning", "-autoexit", str(filein)]

        proc = await asyncio.create_subprocess_exec(*cmd)

        ret = await proc.wait()

        if ret != 0:
            print(filein, "playback failure", file=sys.stderr)

        queue.task_done()


async def main(flist: Iterable[Path]):

    Ntask = os.cpu_count()  # includes logical cores
    if not isinstance(Ntask, int):
        Ntask = 2
    # %% setup queue
    queue = asyncio.Queue()  # type: ignore

    for f in flist:
        await queue.put(f)
    # %% setup Tasks
    if sys.version_info >= (3, 7):
        tasks = [asyncio.create_task(ffplay(queue)) for i in range(Ntask)]
    else:
        tasks = [asyncio.ensure_future(ffplay(queue)) for i in range(Ntask)]

    await queue.join()

    # %% program done, teardown Tasks
    for task in tasks:
        task.cancel()

    await asyncio.gather(*tasks, return_exceptions=True)


def ffplay_sync(qin: queue.Queue):
    """
    Play media synchronously
    """

    while not qin.empty():
        filein = qin.get(timeout=1.0)

        cmd = [FFPLAY, "-v", "warning", "-autoexit", str(filein)]

        ret = subprocess.run(cmd)

        if ret.returncode != 0:
            print(filein, "playback failure", cmd, file=sys.stderr)

        qin.task_done()
