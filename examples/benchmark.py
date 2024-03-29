#!/usr/bin/env python3
"""
simple example of coroutine vs. threading vs. processes

timing on old Windows laptop:

python demo.py c  => 2.3 sec.

python demo.py t  => 2.5 sec.

python demo.py p  => 0.9 sec.

We didn't break out worker setup time from computation time.
In real-world situations, coroutines can be faster and less resource-consuming than threads.
There is no one best choice for all task types,
we fit the asynchronous architecture to the task.
There are numerous other popular implementations of threading and coroutines
beyond the built-in modules used here.

In computation-bound programs like this example, coroutines and threads would
generally not be as good a choice as multiprocessing.
However, the heavier resource usage of multiprocessing is not necessarily best for IO-bound tasks
such as waiting for network connections, where coroutines and/or threads are often a better choice.
"""

import threading
import time
import math
import multiprocessing
import asyncio
from argparse import ArgumentParser


async def coro_worker(i: int, Niter: int, tic: float):
    """coroutine worker"""
    for _ in range(Niter):
        math.sin(3)

    print(f"Coroutine worker {i} done at {time.monotonic() - tic:.2f} sec.")


async def coro(Nworker: int, Niter: int, tic: float):
    tasks = [asyncio.create_task(coro_worker(i, Niter, tic)) for i in range(Nworker)]
    await asyncio.wait(tasks)


class Thread_worker(threading.Thread):
    """threading worker"""

    def __init__(self, i: int, Niter: int):
        super(Thread_worker, self).__init__()
        self.Niter = Niter
        self.i = i

    def run(self):
        tic = time.monotonic()
        for _ in range(self.Niter):
            math.sin(3)

        print(f"Thread worker {i} done at {time.monotonic() - tic:.2f} sec.")


def mp_worker(i: int, Niter: int, tic: float):
    """multiprocessing worker"""
    for _ in range(Niter):
        math.sin(3)

    print(f"Process worker {i} done at {time.monotonic() - tic:.2f} sec.")


if __name__ == "__main__":
    P = ArgumentParser(description="Benchmark coroutines, threads and proceses.")
    P.add_argument(
        "method", choices=["c", "t", "p"], help="c: coroutine, t: threading, p: multiprocessing"
    )
    P.add_argument("-Nworker", help="number of workers", type=int, default=4)
    P.add_argument(
        "-Niter",
        help="number of loop iterations (arbitrary)",
        type=int,
        default=5000000,
    )
    A = P.parse_args()

    ps = []
    ts = []
    tic = time.monotonic()
    for i in range(A.Nworker):
        if A.method == "t":
            t = Thread_worker(i, A.Niter)
            t.start()
            ts.append(t)
        elif A.method == "p":
            p = multiprocessing.Process(target=mp_worker, args=(i, A.Niter, tic))
            p.start()
            ps.append(p)

    if A.method == "c":
        asyncio.run(coro(A.Nworker, A.Niter, tic))
    elif A.method == "p":
        for p in ps:
            p.join()
    elif A.method == "t":
        for t in ts:
            t.join()

    print(f"Elapsed wallclock time: {time.monotonic() - tic:.2f} sec.")
