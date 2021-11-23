import os
from os import path
import shutil

import pytest

from labskit_commands.generate import (parse_project_template, pattern_replacement)
from .utils import get_data_folder


@pytest.fixture
def data_folder():
    return get_data_folder()


def test_generate_1(data_folder):
    """
    Tests the template replacement: Success case
    """
    expected_file = path.join(data_folder, "sample_template.py")

    try:
        pattern_replacement(
            input_file=path.join(data_folder, "sample_template.py.handlebars"),
            mapper={"lib": "pandas", "alias": "pd"}
        )

        assert path.isfile(expected_file)
        with open(expected_file, "r") as f:
            contents = f.read()
            assert "pandas" in contents
            assert "pd" in contents
            assert contents == "import pandas as pd"
    finally:
        os.remove(expected_file)


def test_generate_2(data_folder):
    """
    Tests the template replacement: missing replacement patterns
    """
    expected_file = path.join(data_folder, "sample_template.py")

    try:
        pattern_replacement(
            input_file=path.join(data_folder, "sample_template.py.handlebars"),
            mapper={"lib": "pandas"}
        )

        assert path.isfile(expected_file)
        with open(expected_file, "r") as f:
            contents = f.read()
            assert "pandas" in contents
            assert "{{alias}}" in contents
            assert contents == "import pandas as {{alias}}"
    finally:
        os.remove(expected_file)


def test_generate_3(data_folder):
    """
    Tests the template replacement: No .handlebars
    """
    expected_file = path.join(data_folder, "sample_template")

    pattern_replacement(
        input_file=path.join(data_folder, "sample_template"),
        mapper={"lib": "pandas"}
    )

    assert path.isfile(expected_file)
    with open(expected_file, "r") as f:
        contents = f.read()
        assert len(contents) == 0


def test_generate_4():
    """
    Tests the template replacement: missing replacement patterns
    """
    sub_folder = "sub_folder"
    parameter = "test"
    destination_folder = path.join(os.getcwd(), sub_folder)
    expected_files = [
        path.join(destination_folder, "readme_mlclustering.md"),
        path.join(destination_folder, "tests", "mlclustering", f"test_clustering_{parameter}.py"),
        path.join(destination_folder, "src", f"clustering_{parameter}.py"),
    ]

    try:
        parse_project_template(
            template="mlclustering",
            mapper={"fileName": parameter},
            destination_folder=sub_folder
        )

        for file in expected_files:
            assert path.isfile(file)
    finally:
        shutil.rmtree(destination_folder)
