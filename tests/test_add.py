import os
from gryphon.core import add
from .utils import create_folder_with_venv


TEST_FOLDER = os.path.abspath("")


def test_add_1(setup, teardown, get_pip_libraries):
    lib = "scipy"

    cwd = setup()

    try:
        create_folder_with_venv()
        add(library_name=lib)

        with open(cwd / "requirements.txt") as r:
            requirements = r.read()
            assert lib in requirements

        installed_libs = get_pip_libraries(cwd)

        assert lib in installed_libs

    finally:
        teardown()
