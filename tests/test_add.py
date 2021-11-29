import os
from labskit_commands import add
from .utils import create_folder_with_venv


TEST_FOLDER = os.path.abspath("")


def test_add_1(setup, teardown, get_pip_libraries):
    lib = "scipy"

    absolute_path = setup()

    try:
        create_folder_with_venv(absolute_path)
        add(library_name=lib)

        with open("requirements.txt") as r:
            requirements = r.read()
            assert lib in requirements

        installed_libs = get_pip_libraries()

        assert lib in installed_libs

    finally:
        teardown()
