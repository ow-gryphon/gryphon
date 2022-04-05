import json
import shutil
import os
from os import path

from gryphon.core.registry import Template
from gryphon.core.generate import (
    generate,
    parse_project_template,
    pattern_replacement
)
from .utils import create_folder_with_venv, TEST_FOLDER


def test_generate_1(setup, teardown, data_folder):
    """
    Tests the template replacement: Success case
    """
    file_name = "sample_template.py.handlebars"

    cwd = setup()
    template = data_folder / file_name
    expected_file = cwd / "sample_template.py"
    shutil.copyfile(
        src=template,
        dst=cwd / file_name
    )
    try:
        pattern_replacement(
            input_file=cwd / file_name,
            mapper={"lib": "pandas", "alias": "pd"}
        )

        assert path.isfile(expected_file)
        with open(expected_file, "r") as f:
            contents = f.read()
            assert "pandas" in contents
            assert "pd" in contents
            assert contents == "import pandas as pd"
    finally:
        teardown()


def test_generate_2(setup, teardown, data_folder):
    """
    Tests the template replacement: missing replacement patterns
    """
    file_name = "sample_template.py.handlebars"
    cwd = setup()
    template = data_folder / file_name
    expected_file = cwd / "sample_template.py"
    shutil.copyfile(
        src=template,
        dst=cwd / file_name
    )
    try:
        pattern_replacement(
            input_file=cwd / file_name,
            mapper={"lib": "pandas"}
        )

        assert path.isfile(expected_file)
        with open(expected_file, "r") as f:
            contents = f.read()
        assert "pandas" in contents
        assert "{{alias}}" in contents
        assert contents == "import pandas as {{alias}}"
    finally:
        teardown()


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
        cwd / "readme_mlclustering.md",
        cwd / "src" / f"clustering_{parameter}.py"
    ]

    try:
        parse_project_template(
            template_path=TEST_FOLDER / "data" / "mlclustering" / "template",
            mapper={"fileName": parameter}
        )

        for file in expected_files:
            assert file.is_file()

    finally:
        teardown()


def test_generate_5(setup, teardown, get_pip_libraries):
    try:
        file_name = "test"
        cwd = setup()
        create_folder_with_venv(cwd)
        libraries = get_pip_libraries(cwd)
        assert "scipy" not in libraries

        generate(
            template=Template.template_from_path(TEST_FOLDER / "data" / "mlclustering", type="local"),
            requirements=["scipy"],
            folder=cwd,
            **{"fileName": file_name}
        )

        libraries = get_pip_libraries(cwd)
        assert "scipy" in libraries
        assert (cwd / "readme_mlclustering.md").is_file()
        assert (cwd / "src" / f"clustering_{file_name}.py").is_file()

        log_file = cwd / ".gryphon_history"

        assert log_file.is_file()
        with open(log_file, "r", encoding="utf-8") as f:
            history = json.load(f)
            assert "files" in history
            assert "operations" in history
            assert len(history["operations"]) == 1

    finally:
        teardown()


def test_generate_6(setup, teardown):
    try:
        cwd = setup()
        create_folder_with_venv(cwd)
        template = Template.template_from_path(
            TEST_FOLDER / "data" / "registry_with_git_folder" / "generate",
            type="local"
        )
        generate(
            template=template,
            requirements=[]
        )

        assert not os.path.isdir(cwd / ".git")
        assert not os.path.isfile(cwd / ".git" / "test.txt")

    finally:
        teardown()
