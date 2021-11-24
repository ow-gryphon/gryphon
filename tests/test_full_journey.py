import os
from os import path
import shutil
import pytest

TEST_FOLDER = os.path.abspath("")


def test_full_journey_1():
    folder = "sample_project"
    file_name = "segmentation"
    absolute_path = os.path.join(TEST_FOLDER, folder)
    shutil.rmtree(absolute_path, ignore_errors=True)
    try:
        os.system(f"labskit init analytics {absolute_path}")
        os.chdir(absolute_path)
        os.system(f"labskit generate mlclustering {file_name}")

        assert path.isdir(absolute_path)
        assert path.isdir(path.join(absolute_path, "src"))
        assert path.isdir(path.join(absolute_path, "notebooks"))
        assert path.isdir(path.join(absolute_path, "tests"))

        assert path.isfile(path.join(absolute_path, "src", f"clustering_{file_name}.py"))
    except Exception as e:
        pytest.fail("Raised exception", e)
    finally:
        os.chdir(TEST_FOLDER)
        shutil.rmtree(absolute_path, ignore_errors=True)
