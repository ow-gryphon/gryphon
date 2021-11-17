import os
import shutil
import pytest


def test_full_journey_1():
    folder = "sample_project"
    absolute_path = os.path.abspath(folder)
    shutil.rmtree(absolute_path, ignore_errors=True)
    try:
        os.system(f"labskit init analytics {folder}")
        os.chdir(absolute_path)
        os.system(f"labskit generate mlclustering segmentation")
    except Exception as e:
        pytest.fail("Raised exception", e)
