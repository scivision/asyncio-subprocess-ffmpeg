[![Build Status](https://travis-ci.com/ec500-software-engineering/asyncio-subprocess-ffmpeg.svg?branch=master)](https://travis-ci.com/ec500-software-engineering/asyncio-subprocess-ffmpeg)

# asyncio FFmpeg

Examples of Python asyncio.subprocess with FFmpeg and also traditional synchronous processes.
In general to show the latest techniques, Python &ge; 3.7 is required.

## FFprobe

* `probe_sync`: Use FFprobe to retrieve file metadata synchronously
* `probe_coroutine`: Use FFprobe to retrieve file metadata asynchronously using Python `asyncio` coroutine event loop.

## FFplay

I like to test asynchronous techniques with video playback, as it makes some effects obvious.

* `play_threadpool`: Even though coroutines are more efficient, the syntax of `concurrent.futures.ThreadPoolExecutor` is perhaps the simplest possible way to spawn independent processes in a controlled fashion
* `play_coroutine`: Use Python `asyncio` coroutine event loop to spawn processes.

### Fortran

* `play_coarray.f90`: example of using Fortran with processes and coarrays.

Build by
```sh
cd build
meson ..
ninja
```

run like
```sh
cafrun -np 3 playvid ~/Videos/*
```
