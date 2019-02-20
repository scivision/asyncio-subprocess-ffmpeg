[![Build Status](https://travis-ci.com/ec500-software-engineering/asyncio-subprocess-ffmpeg.svg?branch=master)](https://travis-ci.com/ec500-software-engineering/asyncio-subprocess-ffmpeg)

# asyncio FFmpeg

Examples of Python asyncio.subprocess with FFmpeg and also traditional synchronous processes.
In general to show the latest techniques, Python &ge; 3.7 is required.

## FFprobe

* `probe_sync.py`: Use FFprobe to retrieve file metadata synchronously
* `probe_async.py`: Use FFprobe to retrieve file metadata asynchronously using Python `asyncio`.
