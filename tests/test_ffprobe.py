#!/usr/bin/env python
import pytest
import asyncioffmpeg.ffprobe as probe


@pytest.mark.asyncio
async def test_ffprobe(genpat):

    vid = genpat

    dur = await probe.main(vid)
    assert dur == pytest.approx(5.)


if __name__ == '__main__':
    pytest.main(['-x', __file__])
