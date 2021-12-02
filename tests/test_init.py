from os import path
from labskit_commands.init import init
from .utils import TEST_FOLDER


def test_init_1(setup, teardown):
    cwd = setup()

    try:
        init(
            template_path=path.join(TEST_FOLDER, "data", "analytics"),
            location=cwd
        )
        scr_path = path.join(cwd, "src")
        notebooks_path = path.join(cwd, "notebooks")
        venv_path = path.join(cwd, ".venv")
        requirements_path = path.join(cwd, "requirements.txt")
        gitignore_path = path.join(cwd, ".gitignore")

        assert path.isdir(scr_path)
        assert path.isdir(notebooks_path)
        assert path.isdir(venv_path)
        assert path.isfile(requirements_path)
        assert path.isfile(gitignore_path)

    finally:
        teardown()
