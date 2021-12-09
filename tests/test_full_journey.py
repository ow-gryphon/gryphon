import os
import pytest


def test_full_journey_1(setup, teardown):

    # TODO: create testes also for the ADD functionality
    file_name = "segmentation"
    project_folder = "project"
    cwd = setup()
    try:
        os.system(f"labskit init analytics_git {project_folder}")
        os.chdir(project_folder)
        os.system(f"labskit generate mlclustering_git {file_name}")

        assert (cwd / project_folder).is_dir()
        assert (cwd / project_folder / "src").is_dir()
        assert (cwd / project_folder / "notebooks").is_dir()
        assert (cwd / project_folder / "tests").is_dir()
        assert (cwd / project_folder / "src" / f"clustering_{file_name}.py").is_file()

    except Exception as e:
        pytest.fail("Raised exception", e)
    finally:
        teardown()
