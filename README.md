# asyncio FFmpeg

[![Actions Status](https://github.com/scivision/asyncio-subprocess-ffmpeg/workflows/ci/badge.svg)](https://github.com/scivision/asyncio-subprocess-ffmpeg/actions)

Examples of Python asyncio.subprocess with FFmpeg and also traditional synchronous processes.

## FFprobe

Both synchronous (traditional for loop) and asynchronous pipeline are demonstrated.
They call FFprobe executable to return JSON formatted metadata.

### probe_sync.py

retrieve file metadata synchronously.

### probe_coroutine.py

retrieve file metadata in an asynchronous pipeline (asyncio generator) using Python `asyncio` coroutine event loop.

## FFplay

Test ingasynchronous techniques with video playback makes some effects obvious.
The FFplay asyncio example is more advanced than the FFprobe example.
In the FFprobe example, the lazy asyncio generator produces metadata concurrently as fast as it's requested.
There is no resource throttling in the FFprobe example, so the CPU could become overwhelmed with context switching.

The FFplay example in contrast is an example of a task using resource throttling via asyncio.Queue.
The queueing could also be implemented for FFprobe style task if desired.
However, the rationale employed is that the FFprobe task is overall lightweight, and thus other parts of the pipeline inherently limit resource utilization.
If the FFprobe task was in an asyncio.gather() algorithm, resource utilization could get too high.
Thus we have a "win-win" by using asyncio generator for FFprobe--the throttling comes implicitly from other parts of the pipeline.


### play_threadpool.py

Even though coroutines are more efficient in many applications, the syntax of `concurrent.futures.ThreadPoolExecutor` is perhaps the simplest possible way to spawn independent processes in a controlled fashion

### play_coroutine.py

Use Python `asyncio` coroutine event loop to spawn processes.

### Fortran

* `play_coarray.f90`: example of using Fortran with processes and coarrays.

Build by

```sh
meson build
meson test -C build
```

run like
```sh
cafrun -np 3 playvid ~/Videos/*
```
