import os
import sys
import asyncio


def runner(fun, *args):
    """
    Generic asyncio.run() that handles Windows quirks
    """
    if os.name == "nt" and (3, 7) <= sys.version_info < (3, 8):
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    return asyncio.run(fun(*args))
