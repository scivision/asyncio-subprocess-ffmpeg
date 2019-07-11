#!/usr/bin/env python
"""
simple example of coroutine vs. threading vs. processes

timing on old Windows laptop:

    python demo.py c

    8.6 sec.

    python demo.py t

    9.2 sec.

    python demo.py p

    4.5 sec.   # multiple CPU cores used simultaneously


We didn't break out worker setup time from computation time.
In real-world situations, coroutines can be faster and less resource-consuming than threads.
There is no one best choice for all task types, we fit the asynchronous architecture to the task.
There are numerous other popular implementations of threading and coroutines beyond the built-in modules used here.

In computation-bound programs like this example, coroutines and threads would generally not be as good a choice
as multiprocessing. However, the heavier resource usage of multiprocessing is not necessarily best for IO-bound tasks
such as waiting for network connections, where coroutines and/or threads are often a better choice.
"""
import threading
import time
import math
import multiprocessing
import asyncio
import sys
from argparse import ArgumentParser
from asyncioffmpeg.runner import runner


async def coro_worker(i: int, Niter: int, tic: float):
    """coroutine worker"""
    for _ in range(Niter):
        math.sin(3)

    print("Coroutine worker {} done at {:.2f} sec.".format(i, time.monotonic() - tic))


async def coro(Nworker: int, Niter: int, tic: float):
    if sys.version_info >= (3, 7):
        tasks = [
            asyncio.create_task(coro_worker(i, Niter, tic)) for i in range(Nworker)
        ]
    else:
        tasks = [
            asyncio.ensure_future(coro_worker(i, Niter, tic)) for i in range(Nworker)
        ]
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

        print(
            "Thread worker {} done at {:.2f} sec.".format(
                self.i, time.monotonic() - tic
            )
        )


def mp_worker(i: int, Niter: int, tic: float):
    """ multiprocessing worker"""
    for _ in range(Niter):
        math.sin(3)

    print("Process worker {} done at {:.2f} sec.".format(i, time.monotonic() - tic))


if __name__ == "__main__":
    P = ArgumentParser(
        description="Demonstrate differences between coroutines, threads and proceses."
    )
    P.add_argument("method", help="c: coroutine, t: threading, p: multiprocessing")
    P.add_argument("-Nworker", help="number of workers", type=int, default=4)
    P.add_argument(
        "-Niter",
        help="number of loop iterations (arbitrary)",
        type=int,
        default=5000000,
    )
    A = P.parse_args()

    if A.method not in ("c", "t", "p"):
        raise ValueError("Method must be one of: c t p")

    tic = time.monotonic()
    for i in range(A.Nworker):
        if A.method == "t":
            p = Thread_worker(i, A.Niter)  # type: ignore
            p.start()
        elif A.method == "p":
            p = multiprocessing.Process(  # type: ignore
                target=mp_worker, args=(i, A.Niter, tic)  # type: ignore
            )
            p.start()
            print(
                "started process workert {}, PID: {}".format(i, p.pid)  # type: ignore
            )  # type: ignore

    if A.method == "c":
        runner(coro, A.Nworker, A.Niter, tic)
    else:
        p.join()

    print("{:.2f} sec.".format(time.monotonic() - tic))
