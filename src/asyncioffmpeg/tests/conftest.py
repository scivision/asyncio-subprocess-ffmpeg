import subprocess
from pathlib import Path
import pytest
import shutil

DUR = "5"

EXE = shutil.which("ffmpeg")
if not EXE:
    raise FileNotFoundError("ffmpeg not found")


@pytest.fixture
def genpat(tmp_path) -> Path:
    """
    generate test video
    """

    vidfn = tmp_path / "bars.avi"

    subprocess.check_call(
        [EXE, "-loglevel", "warning", "-f", "lavfi", "-i", "smptebars", "-t", DUR, str(vidfn)]
    )

    return vidfn
