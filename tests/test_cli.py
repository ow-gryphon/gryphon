import os
import pytest
from tests.ui_interaction.init import wizard_init
from tests.ui_interaction.generate import wizard_generate
from tests.ui_interaction.add import wizard_add


def test_cli_1(setup, teardown, get_pip_libraries):

    file_name = "segmentation"
    project_folder = "project"
    lib_name = "scipy"

    cwd = setup()

    try:
        os.system(f"gryph init analytics_git {project_folder}")
        os.chdir(project_folder)
        os.system(f"gryph generate mlclustering_git {file_name}")
        os.system(f"gryph add {lib_name}")
        os.chdir(cwd)

        assert (cwd / project_folder).is_dir()
        assert (cwd / project_folder / "src").is_dir()
        assert (cwd / project_folder / "notebooks").is_dir()
        assert (cwd / project_folder / "tests").is_dir()
        assert (cwd / project_folder / "src" / f"clustering_{file_name}.py").is_file()
        assert lib_name in get_pip_libraries(cwd / project_folder)
    except Exception as e:
        pytest.fail("Raised exception", e)
    finally:
        teardown()


def test_wizard_1(setup, install_gryphon, teardown, get_pip_libraries):

    file_name = "segmentation"
    project_folder = "project"
    lib_name = "scipy"

    cwd = setup()
    # install_gryphon(cwd)
    try:
        wizard_init(project_folder)
        assert (cwd / project_folder).is_dir()
        assert (cwd / project_folder / "notebooks").is_dir()
        assert (cwd / project_folder / "tests").is_dir()

        os.chdir(cwd / project_folder)
        wizard_generate(file_name)
        assert (cwd / project_folder / "src" / "analysis" / f"model_{file_name}.py").is_file()

        wizard_add(lib_name)
        os.chdir(cwd)
        assert lib_name in get_pip_libraries(cwd / project_folder)

    except Exception as e:
        pytest.fail("Raised exception", e)
    finally:
        teardown()

# TODO: Test installation.
