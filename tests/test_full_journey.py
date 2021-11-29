import os
from os import path
import pytest

TEST_FOLDER = os.path.abspath("")


def test_full_journey_1(setup, teardown):
    file_name = "segmentation"
    project_folder = "project"
    cwd = setup()
    try:
        os.system(f"labskit init analytics {project_folder}")
        os.chdir(project_folder)
        os.system(f"labskit generate mlclustering {file_name}")

        assert path.isdir(path.join(cwd, project_folder))
        assert path.isdir(path.join(cwd, project_folder, "src"))
        assert path.isdir(path.join(cwd, project_folder, "notebooks"))
        assert path.isdir(path.join(cwd, project_folder, "tests"))
        assert path.isfile(path.join(cwd, project_folder, "src", f"clustering_{file_name}.py"))

    except Exception as e:
        pytest.fail("Raised exception", e)
    finally:
        teardown()
