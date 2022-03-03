import json
import os
from tests.ui_interaction.init import wizard_init
from tests.ui_interaction.generate import wizard_generate
from tests.ui_interaction.add import wizard_add_typing, wizard_add_matplotlib


def test_cli_1(setup, teardown, get_pip_libraries):

    file_name = "segmentation"
    project_folder = "project"
    lib_name = "matplotlib"

    cwd = setup()

    try:
        os.system(f"gryph init basic_analytics {cwd / project_folder}")
        os.chdir(cwd / project_folder)
        os.system(f"cd {cwd / project_folder} && gryph generate explore_data_basic {file_name}")
        os.system(f"cd {cwd / project_folder} && gryph add {lib_name}")
        os.chdir(cwd)

        assert (cwd / project_folder).is_dir()
        assert (cwd / project_folder / "notebooks").is_dir()

        libs = get_pip_libraries(cwd / project_folder)
        assert lib_name in libs
    finally:
        teardown()


def test_wizard_1(setup, install_gryphon, teardown, get_pip_libraries):

    project_folder = "project"
    lib_name = "scikit-learn"

    cwd = setup()
    # install_gryphon(cwd)

    try:
        wizard_init(cwd)
        assert (cwd / "notebooks").is_dir()
        assert (cwd / "data").is_dir()

        os.chdir(cwd)
        wizard_generate(cwd)

        wizard_add_typing(cwd, lib_name)
        wizard_add_matplotlib(cwd)

        libs = get_pip_libraries(cwd)
        assert "sklearn" in libs
        assert "matplotlib" in libs

        with open(cwd / project_folder / ".gryphon_history", "r", encoding="utf-8") as f:
            history = json.load(f)
            assert "files" in history
            assert "operations" in history
            assert len(history["operations"]) == 4

    finally:
        teardown()
