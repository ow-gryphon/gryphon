import os
import pytest
from tests.ui_interaction.init import wizard_init
from tests.ui_interaction.generate import wizard_generate
from tests.ui_interaction.add import wizard_add_typing, wizard_add_matplotlib


def test_cli_1(setup, teardown, get_pip_libraries):

    file_name = "segmentation"
    project_folder = "project"
    lib_name = "scikit-learn"

    cwd = setup()

    try:
        os.system(f"gryph init basic_analytics {project_folder}")
        os.chdir(project_folder)
        os.system(f"gryph generate customer_segmentation {file_name}")
        os.system(f"gryph add {lib_name}")
        os.chdir(cwd)

        assert (cwd / project_folder).is_dir()
        assert (cwd / project_folder / "src").is_dir()
        assert (cwd / project_folder / "notebooks").is_dir()
        assert (cwd / project_folder / "tests").is_dir()
        assert (cwd / project_folder / "src" / f"clustering_{file_name}.py").is_file()

        # TODO: Find way to activate venv before running add command
        # assert lib_name in get_pip_libraries(cwd / project_folder)
    except Exception as e:
        pytest.fail("Raised exception", e)
    finally:
        teardown()


def test_wizard_1(setup, install_gryphon, teardown, get_pip_libraries):

    file_name = "segmentation"
    project_folder = "project"
    lib_name = "scikit-learn"

    cwd = setup()
    # install_gryphon(cwd)
    try:
        wizard_init(project_folder)
        assert (cwd / project_folder).is_dir()
        assert (cwd / project_folder / "notebooks").is_dir()
        assert (cwd / project_folder / "data").is_dir()

        os.chdir(cwd / project_folder)
        wizard_generate(file_name)

        # assert (cwd / project_folder / "src" / "analysis" / f"model_{file_name}.py").is_file()
        assert os.path.isfile(cwd / project_folder / "template.txt")#.is_file()

        wizard_add_typing(lib_name)
        wizard_add_matplotlib()
        # TODO: Find way to activate venv before running add command
        # assert lib_name in get_pip_libraries(cwd / project_folder)
        # assert "matplotlib" in get_pip_libraries(cwd / project_folder)
    #
    # except Exception as e:
    #     pytest.fail("Raised exception", e)
    finally:
        teardown()
