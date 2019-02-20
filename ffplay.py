#!/usr/bin/env python
"""
This example uses a finite number of workers, rather than slamming the system with endless subprocesses.
This is more effective than endless context switching for an overloaded CPU.
"""
import asyncio
from pathlib import Path
import shutil
import sys
from argparse import ArgumentParser
from typing import List, Generator, Union
import os

if sys.version_info < (3, 7):
    raise RuntimeError('Python >= 3.7 required')


FFPLAY = shutil.which('ffplay')
if not FFPLAY:
    raise FileNotFoundError('FFPLAY not found')


async def ffplay(queue: asyncio.Queue):
    """ Play media asynchronously """
    assert isinstance(FFPLAY, str)

    while True:
        filein = await queue.get()
        assert isinstance(filein, Path)

        cmd = [FFPLAY, '-v', 'warning', '-autoexit', str(filein)]

        proc = await asyncio.create_subprocess_exec(*cmd)

        ret = await proc.wait()

        if ret != 0:
            print(filein, 'playback failure', file=sys.stderr)

        queue.task_done()


async def main(flist: Union[List[Path], Generator[Path, None, None]]):

    Ntask = os.cpu_count()  # includes virtual cores
    if not isinstance(Ntask, int):
        Ntask = 2
# %% setup queue
    queue = asyncio.Queue()  # type: ignore

    for f in flist:
        await queue.put(f)
# %% setup Tasks
    tasks = [asyncio.create_task(ffplay(queue)) for i in range(Ntask)]

    await queue.join()

# %% program done, teardown Tasks
    for task in tasks:
        task.cancel()

    await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == '__main__':
    p = ArgumentParser(
        description="Plays media files asynchronously with FFplay")
    p.add_argument('path', help='directory where media files are kept')
    p.add_argument('-suffix', help='file suffixes of desired media file types',
                   nargs='+', default=['.mp4', '.avi', '.ogv'])
    P = p.parse_args()

    path = Path(P.path).expanduser()
    if not path.is_dir():
        raise FileNotFoundError(f'{path} is not a directory')

    flist = (f for f in path.iterdir() if f.is_file() and f.suffix in P.suffix)

    asyncio.run(main(flist))
