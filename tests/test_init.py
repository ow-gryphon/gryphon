import json
from gryphon.core.init import init
from .utils import TEST_FOLDER


def test_init_1(setup, teardown):
    cwd = setup()
    project = cwd / "project"

    try:
        init(
            template_path=TEST_FOLDER / "data" / "analytics",
            location=project
        )
        scr_path = project / "src"
        notebooks_path = project / "notebooks"
        venv_path = project / ".venv"
        requirements_path = project / "requirements.txt"
        gitignore_path = project / ".gitignore"

        assert scr_path.is_dir()
        assert notebooks_path.is_dir()
        assert venv_path.is_dir()

        assert requirements_path.is_file()
        assert gitignore_path.is_file()

    finally:
        teardown()
