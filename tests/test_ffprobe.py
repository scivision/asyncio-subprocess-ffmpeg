#!/usr/bin/env python
import os
import pytest
import asyncioffmpeg.ffprobe as probe


def get_duration(meta: dict) -> float:
    return float(meta['streams'][0]['duration'])


@pytest.mark.asyncio
@pytest.mark.skipif(os.name == 'nt', reason='Pytest-asyncio not setup for Windows yet')
async def test_ffprobe(genpat):
    vid = genpat

    async for meta in probe.get_meta([vid]):
        assert get_duration(meta) == pytest.approx(5.)


def test_ffprobe_sync(genpat):
    vid = genpat

    meta = probe.ffprobe_sync(vid)
    assert get_duration(meta) == pytest.approx(5.)


if __name__ == '__main__':
    pytest.main(['-x', __file__])
