"""
File containing operations that are common to the commands.
"""
import os
import sys
import json
import glob
import logging
import platform
import errno
import stat
import shutil
import zipfile
from datetime import datetime
from pathlib import Path
import git
from .core_text import Text
from ..constants import (
    SUCCESS, VENV_FOLDER, ALWAYS_ASK, GRYPHON_HOME,
    GENERATE, INIT, SYSTEM_DEFAULT, CONFIG_FILE, DEFAULT_PYTHON_VERSION
)

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
def on_error(func, path, exc):
    value = exc[1]  # os.rmdir
    if func in (os.unlink,  os.remove) and value.errno == errno.EACCES:
        os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)  # 0777
        try:
            func(path)
        except PermissionError:
            logger.error(f"Permission error on {path}. Something might go wrong.")
            pass
    else:
        if func == os.rmdir:
            shutil.rmtree(path)
            return
        raise RuntimeError("File permission error.")


def remove_folder(folder: Path):
    """
    Removes a folder (location relative to cwd or absolute).
    """
    shutil.rmtree(folder, ignore_errors=False, onerror=on_error)


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
        dst=rf'{str(template_destiny)}',
        dirs_exist_ok=True
    )


def execute_and_log(command):
    logger.debug(f"command: {command}")
    cmd = os.popen(command)
    output = cmd.read()
    for line in output.split('\n'):
        logger.debug(line)

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

def create_venv(folder=None, python_version=None):
    """Function to a virtual environment inside a folder."""
    python_path = "python"
    if python_version and python_version != ALWAYS_ASK:

        if python_version != SYSTEM_DEFAULT:

            env_folder = GRYPHON_HOME / f"reserved_env_python_{python_version}"
            if not env_folder.is_dir():
                logger.info(f"Installing python version with Conda.")
                create_conda_env(
                    folder=GRYPHON_HOME / f"reserved_env_python_{python_version}",
                    python_version=python_version
                )

            if platform.system() == "Windows":
                # On Windows the venv folder structure is different from unix
                python_path = env_folder / "envs" / "python.exe"
            else:
                python_path = env_folder / "envs" / "bin" / "python"

    target_folder = get_destination_path(folder)
    venv_path = target_folder / VENV_FOLDER

    # Create venv
    logger.info(f"Creating virtual environment in {venv_path}")
    return_code = execute_and_log(f"\"{python_path}\" -m venv \"{venv_path}\"")
    if return_code:
        raise RuntimeError("Failed to create virtual environment.")

    logger.log(SUCCESS, "Done creating virtual environment.")


def install_libraries_venv(folder=None):
    """
    Function to install the libraries from a 'requirements.txt' file
    """
    target_folder = get_destination_path(folder)
    requirements_path = target_folder / REQUIREMENTS

    if platform.system() == "Windows":
        # On Windows the venv folder structure is different from unix
        pip_path = target_folder / VENV_FOLDER / "Scripts" / "pip.exe"
    else:
        pip_path = target_folder / VENV_FOLDER / "bin" / "pip"

    # Install requirements
    logger.info("Installing requirements. This may take several minutes ...")

    if not pip_path.is_file():
        raise RuntimeError(f"Virtual environment not found inside folder. Should be at {pip_path}")

    if not requirements_path.is_file():
        raise FileNotFoundError("requirements.txt file not found.")

    return_code = execute_and_log(f'\"{pip_path}\" install -r \"{requirements_path}\" --disable-pip-version-check')
    if return_code is not None:
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
        pip_path = target_folder / VENV_FOLDER / "Scripts" / "pip.exe"
        activate_env_command = target_folder / VENV_FOLDER / "Scripts" / "activate.bat"
        silent = "START /B \"\""
        # redirect = ">> .output 2>&1"
        redirect = ">nul 2>&1"
    else:
        pip_path = target_folder / VENV_FOLDER / "bin" / "pip"
        activate_path = target_folder / VENV_FOLDER / "bin" / "activate"
        activate_env_command = str(activate_path)
        os.system(f"chmod 777 \"{activate_path}\"")
        silent = "nohup"
        redirect = ""

    # Install requirements
    logger.info("Installing extra notebook extensions.")

    if not pip_path.is_file():
        raise RuntimeError(f"Virtual environment not found inside folder. Should be at {pip_path}")

    if not requirements_path.is_file():
        raise FileNotFoundError("requirements.txt file not found.")

    with open(requirements_path, "r", encoding="UTF-8") as f1:
        requirements = f1.read()

    for lib in ["jupyter_nbextensions_configurator", "jupyter_contrib_nbextensions"]:
        if lib not in requirements:
            with open(requirements_path, "a", encoding="UTF-8") as f2:
                f2.write(f"\n{lib}")

    return_code = execute_and_log(f'\"{activate_env_command}\" && pip --disable-pip-version-check '
                                  f'install jupyter_contrib_nbextensions jupyter_nbextensions_configurator')

    if return_code is not None:
        raise RuntimeError(f"Failed on pip install command. Return code: {return_code}")

    os.chdir(target_folder)
    return_code = execute_and_log(
        f"\"{activate_env_command}\" "
        f"&& ({silent} jupyter nbextensions_configurator enable --user) {redirect}"
        f"&& ({silent} jupyter contrib nbextension install --user) {redirect}"
        f"&& ({silent} jupyter nbextension enable codefolding/main --user) {redirect}"
        f"&& ({silent} jupyter nbextension enable toc2/main --user) {redirect}"
        f"&& ({silent} jupyter nbextension enable collapsible_headings/main --user) {redirect}"
    )

    if return_code is not None:
        raise RuntimeError(f"Failed to install jupyter nbextensions. Return code: {return_code}")

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

                ANACONDA PROMPT/COMMAND PROMPT:

                >> cd \"{target_folder}\"
                >> .venv\\Scripts\\activate.bat
                
                GIT BASH:
                
                >> cd \"{str(target_folder).replace(chr(92),'/')}\"
                >> source .venv/Scripts/activate

                {Text.install_end_message_2}
            """)
        else:
            logger.info("Opening your new project folder and activating virtual environment.")

            activate_path = target_folder / VENV_FOLDER / "bin" / "activate"
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
    execute_and_log("conda config --set notify_outdated_conda false")
    execute_and_log("conda config --append channels conda-forge --json >> out.json")
    os.remove("out.json")

    command = f"conda create --prefix=\"{conda_path}\" -y -k"

    if python_version and python_version != SYSTEM_DEFAULT:
        command += f" python={python_version}"

    return_code = execute_and_log(command)
    if return_code is not None:
        raise RuntimeError(f"Failed to create conda environment. Status code: {return_code}")

    logger.log(SUCCESS, "Done creating virtual environment.")


def install_libraries_conda(folder=None):
    logger.info("Installing requirements. This may take several minutes ...")
    target_folder = get_destination_path(folder)

    requirements_path = target_folder / "requirements.txt"
    conda_path = target_folder / 'envs'

    execute_and_log("conda config --set notify_outdated_conda false")
    return_code = execute_and_log(f"conda install --prefix \"{conda_path}\" --file \"{requirements_path}\" -k -y")

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

    with open(requirements_path, "r", encoding="UTF-8") as f1:
        requirements = f1.read()

    for lib in ["jupyter_nbextensions_configurator", "jupyter_contrib_nbextensions"]:
        if lib not in requirements:
            with open(requirements_path, "a", encoding="UTF-8") as f2:
                f2.write(f"\n{lib}")

    if platform.system() == "Windows":
        # On Windows the venv folder structure is different from unix
        conda_python = conda_path / "python.exe"
        silent = "START /B \"\""
        # redirect = ">> .output 2>&1"
        redirect = ">nul 2>&1"
    else:
        conda_python = conda_path / "bin" / "python"
        silent = "nohup"
        redirect = ""

    execute_and_log("conda config --set notify_outdated_conda false")
    return_code = execute_and_log(f'conda install jupyter_contrib_nbextensions '
                                  f'jupyter_nbextensions_configurator --prefix=\"{conda_path}\" --yes -k')

    if return_code is not None:
        raise RuntimeError(f"Failed on conda install command. Return code: {return_code}")

    os.chdir(target_folder)

    try:
        return_code = execute_and_log(
            f'({silent} \"{conda_python}\" -m jupyter nbextensions_configurator enable --user) {redirect}')
        assert return_code is None

        return_code = execute_and_log(
            f'({silent} \"{conda_python}\" -m jupyter nbextension enable codefolding/main --user) {redirect}')
        assert return_code is None

        return_code = execute_and_log(
            f'({silent} \"{conda_python}\" -m jupyter contrib nbextension install --user) {redirect}')
        assert return_code is None

        return_code = execute_and_log(
            f'({silent} \"{conda_python}\" -m jupyter nbextension enable toc2/main --user) {redirect}')
        assert return_code is None

        return_code = execute_and_log(
            f'({silent} \"{conda_python}\" -m '
            f'jupyter nbextension enable collapsible_headings/main --user) {redirect}'
        )
        assert return_code is None
        # os.remove("nohup.out")

    except AssertionError:
        raise RuntimeError(f"Failed to install jupyter nbextensions. Return code: {return_code}")

    os.chdir(target_folder.parent)


def change_shell_folder_and_activate_conda_env(location):

    if 'pytest' not in sys.modules:
        target_folder = get_destination_path(location)
        logger.warning(f"""
            {Text.install_end_message_1}

            >> cd {target_folder}
            >> conda activate --prefix=\"{target_folder / "envs"}\"

            {Text.install_end_message_2}
        """)


def update_conda():
    if execute_and_log("conda update conda -k") is not None:
        raise RuntimeError("Failed to update conda.")


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
    path = folder / ".gryphon_history"
    if path.is_file():
        return path

    with open(path, "w", encoding="utf-8") as f:
        f.write("{}")

    return path


def log_new_files(template, performed_action: str, logfile=None):

    assert performed_action in [INIT, GENERATE]
    if logfile is None:
        logfile = Path.cwd() / ".gryphon_history"

    files_and_folders = glob.glob(str(template.path / "template" / "**"), recursive=True)
    files = list(filter(lambda x: x.is_file(), map(Path, files_and_folders)))

    with open(logfile, "r+", encoding="utf-8") as f:
        contents = json.load(f)

        new_contents = contents.copy()
        for file in files:
            new_contents.setdefault("files", []).append(
                dict(
                    path=str(file.relative_to(template.path / "template")),
                    template_name=template.name,
                    version=template.version,
                    action=performed_action,
                    created_at=str(datetime.now())
                )
            )

        f.seek(0)
        f.write(json.dumps(new_contents))
        f.truncate()


def log_operation(template, performed_action: str, logfile=None):

    assert performed_action in [INIT, GENERATE]

    if logfile is None:
        logfile = Path.cwd() / ".gryphon_history"

    with open(logfile, "r+", encoding="utf-8") as f:
        contents = json.load(f)

        new_contents = contents.copy()
        new_contents.setdefault("operations", []).append(
            dict(
                template_name=template.name,
                version=template.version,
                action=performed_action,
                created_at=str(datetime.now())
            )
        )

        f.seek(0)
        f.write(json.dumps(new_contents))
        f.truncate()


def log_add_library(libraries, logfile=None):

    if logfile is None:
        logfile = Path.cwd() / ".gryphon_history"
    try:
        with open(logfile, "r+", encoding="utf-8") as f:
            contents = json.load(f)

            new_contents = contents.copy()
            for lib in libraries:
                new_contents.setdefault("libraries", []).append(
                    dict(
                        name=lib,
                        added_at=str(datetime.now())
                    )
                )

            f.seek(0)
            f.write(json.dumps(new_contents))
            f.truncate()
    except FileNotFoundError:
        raise RuntimeError("The .gryphon_history file was not found, therefore you are not inside a "
                           "Gryphon project directory.")


def get_current_python_version():
    with open(CONFIG_FILE, "r", encoding="UTF-8") as f:
        return json.load(f).get(
            "default_python_version",
            DEFAULT_PYTHON_VERSION
        )


# TEMPLATE DOWNLOAD

def download_template(template) -> Path:
    # TODO: This implementation doesn't address cases where one template depends
    #  on another from a different index

    temp_folder = Path().cwd() / ".temp"
    status_code = execute_and_log(
        f"pip --disable-pip-version-check download {template.name} "
        f"-i {template.template_index} "
        f"-d \"{temp_folder}\" "
        f"--trusted-host ow-gryphon.github.io"  # TODO: Find a definitive solution for this
    )
    if status_code is not None:
        raise RuntimeError("Not able to find the pip command in the environment (required for this feature).")
    return temp_folder


def unzip_templates(path: Path) -> Path:
    zip_files = glob.glob(str(path / "*.zip"))
    target_folder = path / "unzip"
    if target_folder.is_dir():
        os.makedirs(target_folder)

    for file in zip_files:
        with zipfile.ZipFile(file, 'r') as zip_ref:
            zip_ref.extractall(target_folder)
    return target_folder


def unify_templates(target_folder: Path) -> Path:
    expanded_folders = glob.glob(str(target_folder / "*"))
    destination_folder = Path().cwd() / ".target"
    for folder in expanded_folders:
        shutil.copytree(
            src=Path(folder) / "template",
            dst=destination_folder
        )
    return destination_folder
