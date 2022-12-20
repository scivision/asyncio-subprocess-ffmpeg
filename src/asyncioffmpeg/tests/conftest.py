import subprocess
from pathlib import Path
import pytest

from asyncioffmpeg import get_ffmpeg

DUR = "5"


@pytest.fixture
def genpat(tmp_path) -> Path:
    """
    generate test video
    """

    vidfn = tmp_path / "bars.avi"

    subprocess.check_call(
        [
            get_ffmpeg(),
            "-loglevel",
            "warning",
            "-f",
            "lavfi",
            "-i",
            "smptebars",
            "-t",
            DUR,
            str(vidfn),
        ]
    )

    return vidfn
