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
from ..constants import SUCCESS, VENV


logger = logging.getLogger('gryphon')

REQUIREMENTS = "requirements.txt"


# PATH UTILS

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


def quote_windows_path(folder_path):
    return '"' + folder_path + '"'


def escape_windows_path(folder_path):
    return fr'{folder_path}'


# BASH UTILS

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


def copy_project_template(template_source: Path, template_destiny: Path):
    """Copies the templates to destination folder."""

    template_path = template_source / "template"
    template_path.mkdir(exist_ok=True)

    shutil.copytree(
        src=template_path,
        dst=template_destiny,
        dirs_exist_ok=True
    )


def execute_and_log(command):
    cmd = os.popen(command)
    output = cmd.read()
    logger.debug(output)

    # status code
    return cmd.close()


# GIT

def init_new_git_repo(folder: Path) -> git.Repo:
    """Init new git repository on folder."""
    return git.Repo.init(folder)


def initial_git_commit(repository: git.Repo):
    """Does the first git commit."""
    repository.git.add(A=True)
    repository.index.commit("Initial commit")


# VENV

def create_venv(folder=None):
    """Function to a virtual environment inside a folder."""
    target_folder = get_destination_path(folder)
    venv_path = target_folder / VENV

    # Create venv
    logger.info(f"Creating virtual environment in {venv_path}")
    os.system(f"python -m venv \"{venv_path}\"")
    logger.log(SUCCESS, "Done creating virtual environment.")


def install_libraries_venv(folder=None):
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
    logger.info("Installing requirements. This may take several minutes ...")

    if not pip_path.is_file():
        raise RuntimeError(f"Virtual environment not found inside folder. Should be at {pip_path}")

    if not requirements_path.is_file():
        raise FileNotFoundError("requirements.txt file not found.")

    cmd = os.popen(f'{str(pip_path)} install -r {str(requirements_path)}')
    output = cmd.read()
    logger.debug(output)
    return_code = cmd.close()
    if cmd.close() is not None:
        raise RuntimeError(f"Failed on pip install command. Status code: {return_code}")

    logger.log(SUCCESS, "Installation successful!")


def install_extra_nbextensions_venv(folder_path):
    """
        Function to install the libraries from a 'requirements.txt' file
        """
    target_folder = get_destination_path(folder_path)
    requirements_path = target_folder / REQUIREMENTS

    if platform.system() == "Windows":
        # On Windows the venv folder structure is different from unix
        pip_path = target_folder / VENV / "Scripts" / "pip.exe"
        activate_env_command = target_folder / VENV / "Scripts" / "activate.bat"

    else:
        pip_path = target_folder / VENV / "bin" / "pip"
        activate_path = target_folder / VENV / "bin" / "activate"
        activate_env_command = str(activate_path)
        os.system(f"chmod 777 {activate_path}")

    # Install requirements
    logger.info("Installing extra notebook extensions.")

    if not pip_path.is_file():
        raise RuntimeError(f"Virtual environment not found inside folder. Should be at {pip_path}")

    if not requirements_path.is_file():
        raise FileNotFoundError("requirements.txt file not found.")

    with open(requirements_path, "r") as f1:
        requirements = f1.read()

    for lib in ["jupyter_nbextensions_configurator", "jupyter_contrib_nbextensions"]:
        if lib not in requirements:
            with open(requirements_path, "a") as f2:
                f2.write(f"\n{lib}\n")

    try:
        execute_and_log(f'{activate_env_command} && pip install jupyter_contrib_nbextensions')
        execute_and_log(f'{activate_env_command} && pip install jupyter_nbextensions_configurator')

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed on pip install command. {e}")

    os.chdir(target_folder)
    execute_and_log(f"{activate_env_command} && nohup jupyter nbextensions_configurator enable --user")
    execute_and_log(f"{activate_env_command} && nohup jupyter contrib nbextension install --user")
    execute_and_log(f"{activate_env_command} && nohup jupyter nbextension enable codefolding/main --user")
    execute_and_log(f"{activate_env_command} && nohup jupyter nbextension enable toc2/main --user")
    execute_and_log(f"{activate_env_command} && nohup jupyter nbextension enable collapsible_headings/main --user")
    os.chdir(target_folder.parent)


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

                >> cd {target_folder}
                >> .venv/Scripts/activate.bat

                {Text.install_end_message_2}
            """)
        else:
            logger.info("Opening your new project folder and activating virtual environment.")

            activate_path = target_folder / VENV / "bin" / "activate"
            os.chdir(target_folder)

            shell = os.environ.get('SHELL', '/bin/sh')
            os.execl(shell, shell, "--rcfile", activate_path)


# CONDA

def create_conda_env(folder=None, python_version=None):
    """Function to a virtual environment inside a folder."""
    target_folder = get_destination_path(folder)
    conda_path = target_folder / 'envs'

    # Create venv
    logger.info(f"Creating Conda virtual environment in {conda_path}")
    execute_and_log("conda config --append channels conda-forge")
    command = f"conda create --prefix={conda_path} -y"
    if python_version:
        command += f" --python={python_version}"

    return_code = execute_and_log(command)
    if return_code is not None:
        raise RuntimeError(f"Failed to create conda environment. Status code: {return_code}")

    logger.log(SUCCESS, "Done creating virtual environment.")


def install_libraries_conda(folder):
    logger.info("Installing requirements. This may take several minutes ...")
    target_folder = get_destination_path(folder)
    conda_path = target_folder / 'envs'

    return_code = execute_and_log(f"conda install --prefix {conda_path} --file requirements.txt -y")

    if return_code is not None:
        raise RuntimeError(f"Failed to install requirements on conda environment. Status code: {return_code}")

    logger.log(SUCCESS, "Installation successful!")


def install_extra_nbextensions_conda(folder_path):
    """
        Function to install the libraries from a 'requirements.txt' file
        """
    target_folder = get_destination_path(folder_path)
    conda_path = target_folder / 'envs'
    requirements_path = target_folder / REQUIREMENTS

    # Install requirements
    logger.info("Installing extra notebook extensions.")

    if not conda_path.is_dir():
        raise RuntimeError(f"Conda environment not found inside folder. Should be at {conda_path}")

    if not requirements_path.is_file():
        raise FileNotFoundError("requirements.txt file not found.")

    with open(requirements_path, "r") as f1:
        requirements = f1.read()

    for lib in ["jupyter_nbextensions_configurator", "jupyter_contrib_nbextensions"]:
        if lib not in requirements:
            with open(requirements_path, "a") as f2:
                f2.write(f"\n{lib}\n")

    if platform.system() == "Windows":
        # On Windows the venv folder structure is different from unix
        conda_pip = conda_path / "Scripts" / "pip.exe"
        conda_pip = conda_path / "Scripts" / "python.exe"
    else:
        conda_pip = conda_path / "bin" / "pip"
        conda_python = conda_path / "bin" / "python"

    try:
        execute_and_log(f'{conda_pip} install jupyter_contrib_nbextensions')
        execute_and_log(f'{conda_pip} install jupyter_nbextensions_configurator')

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed on pip install command. {e}")

    os.chdir(target_folder)
    execute_and_log(f'nohup {conda_python} -m jupyter nbextensions_configurator enable --user')
    execute_and_log(f'nohup {conda_python} -m jupyter contrib nbextension install --user')
    execute_and_log(f'nohup {conda_python} -m jupyter nbextension enable codefolding/main --user')
    execute_and_log(f'nohup {conda_python} -m jupyter nbextension enable toc2/main --user')
    execute_and_log(f'nohup {conda_python} -m jupyter nbextension enable collapsible_headings/main --user')
    os.chdir(target_folder.parent)


# requirements.txt UTILS

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
                     f"It is required in order to run this command.")


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


# RC FILE

def get_rc_file(folder=Path.cwd()):
    """
    Updates the needed options inside the .labskitrc file.
    """
    path = folder / ".gryphon_log"
    if path.is_file():
        return path

    open(path, "w").close()

    return path


def populate_rc_file(rc_file, action):
    """
    Updates the needed options inside the .labskitrc file.
    """
    with open(rc_file, "a") as f:
        f.write(action + '\n')
