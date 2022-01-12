"""
Utility functions for the test suite.
"""
import os
from pathlib import Path
import platform
import shutil
import subprocess
from gryphon.core.command_operations import (
    create_venv,
    get_destination_path
)
import errno
import stat


TEST_FOLDER = Path("tests").resolve()
VENV = ".venv"


def on_error(func, path, exc):
    value = exc[1] #os.rmdir,
    if func in (os.unlink,  os.remove) and value.errno == errno.EACCES:
        os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)  # 0777
        try:
            func(path)
        except PermissionError:
            pass
    else:
        raise


def remove_folder(folder):
    """
    Removes a folder (location relative to cwd or absolute).
    """
    shutil.rmtree(folder, ignore_errors=False, onerror=on_error)


def create_folder(folder: Path):
    """
    Create a folder in the given path (location relative to cwd or absolute).
    """
    folder.mkdir(exist_ok=True, parents=False)


def create_folder_with_venv(folder_name: Path = None, requirements=None):
    """
    Creates a folder, creates a venv inside it and copies a sample requirements.txt file.
    """
    if folder_name is not None and not folder_name.is_dir():
        create_folder(folder_name)

    create_venv(Path.cwd())
    if requirements is None:
        requirements = get_data_folder() / "sample_requirements.txt"

    destination = get_destination_path(folder_name)

    shutil.copyfile(
        src=requirements,
        dst=destination / "requirements.txt"
    )


def get_data_folder() -> Path:
    return TEST_FOLDER / "data"


def get_pip_path(base_folder=Path.cwd()):
    if platform.system() == "Windows":
        # On windows the venv folder structure is different from unix
        pip_path = base_folder / VENV / "Scripts" / "pip.exe"
    else:
        pip_path = base_folder / VENV / "bin" / "pip"

    return pip_path


def get_requirements_path(base_folder: Path):
    return base_folder / "requirements.txt"


def get_venv_path(base_folder: Path) -> Path:
    return base_folder / VENV


def activate_venv(folder=None):
    """
    Function to activate virtual environment.
    """
    target_folder = get_destination_path(folder)
    try:
        if platform.system() == "Windows":
            # On windows the venv folder structure is different from unix
            activate_path = target_folder / VENV / "Scripts" / "activate.bat"
            command = [str(activate_path)]

        else:
            activate_path = target_folder / VENV / "bin" / "activate"
            command = ['bash', str(activate_path)]

        subprocess.check_call(command)

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to activate venv. {e}")
