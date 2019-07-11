#!/usr/bin/env python
import pytest
import asyncioffmpeg.ffprobe as probe
from asyncioffmpeg.runner import runner


def get_duration(meta: dict) -> float:
    return float(meta["streams"][0]["duration"])


def test_ffprobe_as_completed(genpat):
    vid = genpat

    metas = runner(probe.get_meta, vid.parent, [".avi", ".mp4"])
    assert len(metas) == 1
    assert get_duration(metas[0]) == pytest.approx(5.0)


def test_ffprobe_gather(genpat):
    vid = genpat

    metas = runner(probe.get_meta_gather, vid.parent, [".avi", ".mp4"])
    assert len(metas) == 1
    assert get_duration(metas[0]) == pytest.approx(5.0)


def test_ffprobe_sync(genpat):
    vid = genpat

    meta = probe.ffprobe_sync(vid)
    assert get_duration(meta) == pytest.approx(5.0)


if __name__ == "__main__":
    pytest.main(["-x", __file__])
