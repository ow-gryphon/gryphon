from os import path
import shutil
from labskit_commands.init import init


def test_init_1(setup, teardown):
    cwd = setup()

    try:
        init(
            template="analytics",
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
