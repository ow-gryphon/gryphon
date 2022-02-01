"""
File containing operations that are common to the commands.
"""

import sys
import os
import logging
from pathlib import Path
import platform
import subprocess
import shutil
import git
from .core_text import Text


logger = logging.getLogger('gryphon')

VENV = ".venv"
REQUIREMENTS = "requirements.txt"


def get_destination_path(folder=None) -> Path:
    """
    Function that helps to define the full path to a directory.

    It checks if the path is an absolute or relative path, then
    if relative, it appends the current folder to it, transforming
    it into an absolute path.
    """
    if folder is None:
        return Path.cwd()

    path_obj = Path(folder)

    if not path_obj.is_absolute():
        return path_obj.resolve()

    return path_obj


def create_venv(folder=None):
    """Function to a virtual environment inside a folder."""
    target_folder = get_destination_path(folder)
    venv_path = target_folder / VENV

    # Create venv
    logger.debug(f"Creating virtual environment in {venv_path}")
    os.system(f"python -m venv \"{venv_path}\"")
    logger.info("Done creating virtual environment.")


def quote_windows_path(folder_path):
    return '"' + folder_path + '"'


def escape_windows_path(folder_path):
    return fr'{folder_path}'


def install_extra_nbextensions(folder_path):
    """
        Function to install the libraries from a 'requirements.txt' file
        """
    target_folder = get_destination_path(folder_path)
    requirements_path = target_folder / REQUIREMENTS

    if platform.system() == "Windows":
        # On Windows the venv folder structure is different from unix
        pip_path = target_folder / VENV / "Scripts" / "pip.exe"
    else:
        pip_path = target_folder / VENV / "bin" / "pip"

    # Install requirements
    logger.debug("Installing extra notebook extensions.")

    if not pip_path.is_file():
        raise RuntimeError(f"Virtual environment not found inside folder. Should be at {pip_path}")

    if not requirements_path.is_file():
        raise FileNotFoundError("requirements.txt file not found.")

    with open(requirements_path, "r", encoding='utf-8') as f1:
        requirements = f1.read()

    if "jupyter_contrib_nbextensions" not in requirements:
        with open(requirements_path, "a", encoding='utf-8') as f2:
            f2.write("\njupyter_contrib_nbextensions\n")

    try:
        subprocess.check_call([str(pip_path), 'install', 'jupyter_contrib_nbextensions', '-qq'],)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed on pip install command. {e}")

    os.chdir(target_folder)
    os.system(f"jupyter contrib nbextension install --user --Application.log_level=0")
    os.system(f"jupyter nbextensions_configurator enable --user --Application.log_level=0")
    os.system(f"jupyter nbextension enable codefolding/main --Application.log_level=0")
    os.system(f"jupyter nbextension enable toc2/main --Application.log_level=0")
    os.system(f"jupyter nbextension enable collapsible_headings/main --Application.log_level=0")
    os.chdir(target_folder.parent)


def install_libraries(folder=None):
    """
    Function to install the libraries from a 'requirements.txt' file
    """
    target_folder = get_destination_path(folder)
    requirements_path = target_folder / REQUIREMENTS

    if platform.system() == "Windows":
        # On Windows the venv folder structure is different from unix
        pip_path = target_folder / VENV / "Scripts" / "pip.exe"
    else:
        pip_path = target_folder / VENV / "bin" / "pip"

    # Install requirements
    logger.debug("Installing requirements. This may take several minutes ...")

    if not pip_path.is_file():
        raise RuntimeError(f"Virtual environment not found inside folder. Should be at {pip_path}")

    if not requirements_path.is_file():
        raise FileNotFoundError("requirements.txt file not found.")

    try:
        subprocess.check_call([str(pip_path), 'install', '-r', str(requirements_path), '-qqq'])
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed on pip install command. {e}")

    logger.info("Installation successful!")


def change_shell_folder_and_activate_venv(location):
    if 'pytest' not in sys.modules:
        target_folder = get_destination_path(location)

        if platform.system() == "Windows":
            # On windows the venv folder structure is different from unix
            # activate_path = target_folder / VENV / "Scripts" / "activate.bat"
            # os.system(
            #     f"""start cmd /k "echo Activating virtual environment & """
            #     f"""{activate_path} & """
            #     """echo "Virtual environment activated. Now loading Gryphon" & """
            #     """gryphon" """
            # )

            logger.warning(f"""
                {Text.install_end_message_1}
                
                ANACONDA PROMPT/COMMAND PROMPT
                
                >> cd {target_folder}
                >> .venv\\Scripts\\activate.bat
                
                GIT BASH
                
                >> cd {target_folder}
                >> source .venv/Scripts/activate
                
                {Text.install_end_message_2}
            """)
        else:
            logger.debug("Opening your new project folder and activating virtual environment.")

            activate_path = target_folder / VENV / "bin" / "activate"
            os.chdir(target_folder)

            shell = os.environ.get('SHELL', '/bin/sh')
            os.execl(shell, shell, "--rcfile", activate_path)


def copy_project_template(template_source: Path, template_destiny: Path):
    """Copies the templates to destination folder."""

    template_path = template_source / "template"
    template_path.mkdir(exist_ok=True)
    
    shutil.copytree(
        src=template_path,
        dst=template_destiny,
        dirs_exist_ok=True
    )


def init_new_git_repo(folder: Path) -> git.Repo:
    """Init new git repository on folder."""
    return git.Repo.init(folder)


def initial_git_commit(repository: git.Repo):
    """Does the first git commit."""
    repository.git.add(A=True)
    repository.index.commit("Initial commit")


def append_requirement(library_name):
    """Appends a given requirement to the requirements.txt file."""

    current_path = get_destination_path()
    requirements_path = current_path / REQUIREMENTS
    try:
        with open(requirements_path, "r", encoding='UTF-8') as file:
            requirements = file.read()

        if library_name not in requirements:
            with open(requirements_path, "a", encoding='UTF-8') as file:
                file.write(f"\n{library_name}")

    except FileNotFoundError:
        logger.error(f"Could not find requirements file at {requirements_path}, "
                     f"It is required to run this command.")


def rollback_append_requirement(library_name):
    current_path = get_destination_path()
    requirements_path = current_path / REQUIREMENTS

    assert requirements_path.is_file()

    with open(requirements_path, "r", encoding='UTF-8') as file:
        requirements = file.read()

    requirements_list = requirements.split('\n')
    last_requirement_added = requirements_list[-1]

    if library_name == last_requirement_added:
        with open(requirements_path, "w", encoding='UTF-8') as file:
            file.write('\n'.join(requirements_list[:-1]))


def remove_folder(folder: Path):
    """
    Removes a folder (location relative to cwd or absolute).
    """
    shutil.rmtree(folder, ignore_errors=False)


def create_folder(folder: Path):
    """
    Create a folder in the given path (location relative to cwd or absolute).
    """
    folder.mkdir(exist_ok=True)


def populate_rc_file(folder):
    """
    Updates the needed options inside the .labskitrc file.
    """
    return folder
    # TODO: Create .labskitrc and populate it accordingly