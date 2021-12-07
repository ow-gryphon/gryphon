from os import path
from labskit_commands.init import init
from .utils import TEST_FOLDER


def test_init_1(setup, teardown):
    cwd = setup()

    try:
        init(
            template_path=TEST_FOLDER / "data" / "analytics",
            location=cwd
        )
        scr_path = cwd / "src"
        notebooks_path = cwd / "notebooks"
        venv_path = cwd / ".venv"
        requirements_path = cwd / "requirements.txt"
        gitignore_path = cwd / ".gitignore"

        assert scr_path.is_dir()
        assert notebooks_path.is_dir()
        assert venv_path.is_dir()

        assert requirements_path.is_file()
        assert gitignore_path.is_file()

    finally:
        teardown()
