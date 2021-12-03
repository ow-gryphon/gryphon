import os
from os import path
from labskit_commands.generate import (
    generate,
    parse_project_template,
    pattern_replacement
)
from .utils import create_folder_with_venv, TEST_FOLDER


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


def test_generate_4(setup, teardown):
    """
    Tests the template replacement: missing replacement patterns
    """
    cwd = setup()
    parameter = "test"

    expected_files = [
        path.join(cwd, "readme_mlclustering.md"),
        path.join(cwd, "src", f"clustering_{parameter}.py"),
    ]

    try:
        parse_project_template(
            template_path=path.join(TEST_FOLDER, "data", "mlclustering"),
            mapper={"fileName": parameter}
        )

        for file in expected_files:
            assert path.isfile(file)

    finally:
        teardown()


def test_generate_5(setup, teardown, get_pip_libraries):
    try:
        file_name = "test"
        _ = setup()
        create_folder_with_venv(".")
        libraries = get_pip_libraries()
        assert "scipy" not in libraries

        generate(
            template_path=path.join(TEST_FOLDER, "data", "mlclustering"),
            requirements=["scipy"],
            extra_parameters={"fileName": file_name}
        )

        libraries = get_pip_libraries()
        assert "scipy" in libraries
        assert path.isfile("readme_mlclustering.md")
        assert path.isfile(path.join("src", f"clustering_{file_name}.py"))

    finally:
        teardown()
