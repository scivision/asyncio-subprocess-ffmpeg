from pytest import approx
import asyncio

import asyncioffmpeg.ffprobe as probe


def get_duration(meta: dict) -> float:
    return float(meta["streams"][0]["duration"])


def test_ffprobe_as_completed(genpat):
    vid = genpat

    metas = asyncio.run(probe.get_meta(vid.parent, [".avi", ".mp4"]))
    assert len(metas) == 1
    assert get_duration(metas[0]) == approx(5.0)


def test_ffprobe_gather(genpat):
    vid = genpat

    metas = asyncio.run(probe.get_meta_gather(vid.parent, [".avi", ".mp4"]))
    assert len(metas) == 1
    assert get_duration(metas[0]) == approx(5.0)


def test_ffprobe_sync(genpat):
    vid = genpat

    meta = probe.ffprobe_sync(vid)
    assert get_duration(meta) == approx(5.0)
