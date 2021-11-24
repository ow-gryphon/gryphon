import glob
import os
from os import path
from labskit_commands import add
from .utils import create_folder_with_venv, remove_folder
import pytest


TEST_FOLDER = os.path.abspath("")


def test_add_1():
    lib = "scipy"
    folder = "sample_project"
    prev_folder = os.getcwd()
    absolute_path = os.path.abspath(folder)
    remove_folder(absolute_path)
    try:
        create_folder_with_venv(absolute_path)
        os.chdir(absolute_path)
        add(library_name=lib)

        with open("requirements.txt") as r:
            requirements = r.read()
            assert lib in requirements

        glob_pattern = os.path.join(".venv", "lib*", "python*", "site-packages", "*")
        folders = list(map(os.path.basename, glob.glob(glob_pattern)))

        assert lib in folders

    except Exception as e:
        pytest.fail("Raised exception", e)
    finally:
        os.chdir(prev_folder)
        remove_folder(absolute_path)
