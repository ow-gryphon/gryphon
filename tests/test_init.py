from os import path
import shutil
from labskit_commands.init import init


def test_init_1():
    folder = "sample_folder"
    full_path = path.abspath(folder)

    try:
        init(
            template="analytics",
            location=folder
        )
        scr_path = path.join(full_path, "src")
        notebooks_path = path.join(full_path, "notebooks")
        venv_path = path.join(full_path, ".venv")
        requirements_path = path.join(full_path, "requirements.txt")
        gitignore_path = path.join(full_path, ".gitignore")

        assert path.isdir(scr_path)
        assert path.isdir(notebooks_path)
        assert path.isdir(venv_path)
        assert path.isfile(requirements_path)
        assert path.isfile(gitignore_path)

    finally:
        shutil.rmtree(full_path)
