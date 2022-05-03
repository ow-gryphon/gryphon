"""
File containing operations that are common to the commands.
"""
import errno
import glob
import json
import logging
import os
import platform
import shutil
import stat
import sys
import zipfile
from datetime import datetime
from distutils.version import StrictVersion
from pathlib import Path

import git

from .core_text import Text
from ..constants import (
    SUCCESS, VENV_FOLDER, ALWAYS_ASK, GRYPHON_HOME,
    GENERATE, INIT, SYSTEM_DEFAULT, CONFIG_FILE, DEFAULT_PYTHON_VERSION,
    USE_LATEST
)

logger = logging.getLogger('gryphon')

REQUIREMENTS = "requirements.txt"
GRYPHON_HISTORY = ".gryphon_history"
REQUIREMENTS_NOT_FOUND = "requirements.txt file not found."


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


def execute_and_log(command) -> tuple:
    logger.debug(f"command: {command}")
    cmd = os.popen(command)
    output = cmd.read()
    for line in output.split('\n'):
        logger.debug(line)

    # status code
    return cmd.close(), output


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
    if python_version and python_version not in [ALWAYS_ASK, SYSTEM_DEFAULT]:

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
    return_code, _ = execute_and_log(f"\"{python_path}\" -m venv \"{venv_path}\"")
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
        raise RuntimeError(f"Virtual environment not found inside folder. Should be at {pip_path}."
                           f"\nAre you using venv instead of conda?")

    if not requirements_path.is_file():
        raise FileNotFoundError(REQUIREMENTS_NOT_FOUND)

    return_code, output = execute_and_log(f'\"{pip_path}\" install -r \"{requirements_path}\"'
                                          f' --disable-pip-version-check')
    if return_code is not None:
        # TODO: take the error output from stderr
        if "Could not find a version that satisfies the requirement" in output:
            logger.error(output)
        else:
            logger.error(f"Failed on pip install command. Status code: {return_code}")
    else:
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
        raise RuntimeError(f"Virtual environment not found inside folder. Should be at {pip_path}"
                           f"\nAre you using venv instead of conda?")

    if not requirements_path.is_file():
        raise FileNotFoundError(REQUIREMENTS_NOT_FOUND)

    with open(requirements_path, "r", encoding="UTF-8") as f1:
        requirements = f1.read()

    for lib in ["jupyter_nbextensions_configurator", "jupyter_contrib_nbextensions"]:
        if lib not in requirements:
            with open(requirements_path, "a", encoding="UTF-8") as f2:
                f2.write(f"\n{lib}")

    return_code, _ = execute_and_log(
        f'\"{activate_env_command}\" && pip --disable-pip-version-check install '
        f'jupyter_contrib_nbextensions jupyter_nbextensions_configurator'
    )

    if return_code is not None:
        raise RuntimeError(f"Failed on pip install command. Return code: {return_code}")

    os.chdir(target_folder)
    return_code, _ = execute_and_log(
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
        logger.warning(f"""
                        {Text.install_end_message_1}

                        ANACONDA PROMPT/COMMAND PROMPT:

                        >> cd \"{target_folder}\"
                        >> .venv\\Scripts\\activate.bat

                        GIT BASH:

                        >> cd \"{str(target_folder).replace(chr(92), '/')}\"
                        >> source .venv/Scripts/activate

                        {Text.install_end_message_2}
                    """)

        # if platform.system() == "Windows":
        #     On windows the venv folder structure is different from unix
        #     activate_path = target_folder / VENV / "Scripts" / "activate.bat"
        #     os.system(
        #         f"""start cmd /k "echo Activating virtual environment & """
        #         f"""{activate_path} & """
        #         """echo "Virtual environment activated. Now loading Gryphon" & """
        #         """gryphon" """
        #     )
        # else:
        #     logger.info("Opening your new project folder and activating virtual environment.")
        #
        #     activate_path = target_folder / VENV_FOLDER / "bin" / "activate"
        #     os.chdir(target_folder)
        #
        #     shell = os.environ.get('SHELL', '/bin/sh')
        #     os.execl(shell, shell, "--rcfile", activate_path)


# CONDA

def create_conda_env(folder=None, python_version=None):
    """Function to a virtual environment inside a folder."""
    target_folder = get_destination_path(folder)
    conda_path = target_folder / 'envs'

    # Create venv
    logger.info(f"Creating Conda virtual environment in {conda_path}")
    execute_and_log("conda config --append channels conda-forge --json >> out.json")
    if Path("out.json").is_file():
        os.remove("out.json")

    command = f"conda create --prefix=\"{conda_path}\" -y -k"
    # TODO: Verificar essa terceira condição aqui
    if python_version and python_version != SYSTEM_DEFAULT and python_version != ALWAYS_ASK:
        command += f" python={python_version}"

    return_code, _ = execute_and_log(command)
    if return_code is not None:
        raise RuntimeError(f"Failed to create conda environment. Status code: {return_code}")

    logger.log(SUCCESS, "Done creating virtual environment.")


def install_libraries_conda(folder=None):
    """
        TODO:  Mensagem achada quando pedimos uma versão que nao existe usando conda
        PackagesNotFoundError: The following packages are not available from current channels:

          - matplotlib==1.5.8

        Current channels:

          - https://repo.anaconda.com/pkgs/main/linux-64
          - https://repo.anaconda.com/pkgs/main/noarch
          - https://repo.anaconda.com/pkgs/r/linux-64
          - https://repo.anaconda.com/pkgs/r/noarch
          - https://conda.anaconda.org/conda-forge/linux-64
          - https://conda.anaconda.org/conda-forge/noarch

        To search for alternate channels that may provide the conda package you're
        looking for, navigate to
    """
    logger.info("Installing requirements. This may take several minutes ...")
    target_folder = get_destination_path(folder)

    requirements_path = target_folder / REQUIREMENTS
    conda_path = target_folder / 'envs'

    if not conda_path.is_dir():
        raise RuntimeError(f"Conda environment not found inside folder. Should be at {conda_path}"
                           f"\nAre you using conda instead of venv?")

    return_code, output = execute_and_log(f"conda install --prefix \"{conda_path}\""
                                          f" --file \"{requirements_path}\" -k -y")

    if return_code is not None:
        # TODO: take the error output from stderr
        if "Could not find a version that satisfies the requirement" in output:
            logger.error(output)
        else:
            logger.error(f"Failed on pip install command. Status code: {return_code}")
    else:
        logger.log(SUCCESS, "Installation successful!")

    # if return_code is not None:
    #     raise RuntimeError(f"Failed to install requirements on conda environment. Status code: {return_code}")
    # logger.log(SUCCESS, "Installation successful!")


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
        raise RuntimeError(f"Conda environment not found inside folder. Should be at {conda_path}"
                           f"\nAre you using conda instead of venv?")

    if not requirements_path.is_file():
        raise FileNotFoundError(REQUIREMENTS_NOT_FOUND)

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
        redirect = ">nul 2>&1"
    else:
        conda_python = conda_path / "bin" / "python"
        silent = "nohup"
        redirect = ""

    return_code, _ = execute_and_log(
        f'conda install jupyter_contrib_nbextensions '
        f'jupyter_nbextensions_configurator --prefix=\"{conda_path}\" --yes -k'
    )

    if return_code is not None:
        raise RuntimeError(f"Failed on conda install command. Return code: {return_code}")

    os.chdir(target_folder)

    try:
        return_code, _ = execute_and_log(
            f'({silent} \"{conda_python}\" -m jupyter nbextensions_configurator enable --user) {redirect}')
        assert return_code is None

        return_code, _ = execute_and_log(
            f'({silent} \"{conda_python}\" -m jupyter nbextension enable codefolding/main --user) {redirect}')
        assert return_code is None

        return_code, _ = execute_and_log(
            f'({silent} \"{conda_python}\" -m jupyter contrib nbextension install --user) {redirect}')
        assert return_code is None

        return_code, _ = execute_and_log(
            f'({silent} \"{conda_python}\" -m jupyter nbextension enable toc2/main --user) {redirect}')
        assert return_code is None

        return_code, _ = execute_and_log(
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
    if execute_and_log("conda update conda -k -y")[0] is not None:
        raise RuntimeError("Failed to update conda.")


# requirements.txt UTILS

def get_library_name(library_name):
    """
    Utility to split between the library name and version number when needed
    """
    name = library_name
    for sign in ['!=', '==', '>=', '~=']:
        name = name.split(sign)[0]
    return name.strip()


def append_requirement(library_name, location=Path.cwd()):
    """Appends a given requirement to the requirements.txt file."""

    name = get_library_name(library_name)
    current_path = get_destination_path(location)
    requirements_path = current_path / REQUIREMENTS
    try:
        with open(requirements_path, "r", encoding='UTF-8') as file:
            requirements = file.read()

    except FileNotFoundError:
        requirements = ""
        with open(requirements_path, "w", encoding='UTF-8') as file:
            file.write("")

    # check if the library was already installed
    lib_list = requirements.split("\n")
    exclusion_list = []
    for index, lib in enumerate(lib_list):
        if name == get_library_name(lib):
            exclusion_list.append(index)

    for r_index in exclusion_list[::-1]:
        lib_list.pop(r_index)

    lib_list.append(library_name)

    with open(requirements_path, "r+", encoding='UTF-8') as f:
        f.seek(0)
        f.write("\n".join(lib_list))
        f.truncate()


def backup_requirements(cwd=Path.cwd()):

    current_path = get_destination_path(cwd)
    requirements_path = current_path / REQUIREMENTS
    backup_path = current_path / "requirements.backup"

    with open(requirements_path, "r", encoding="UTF-8") as f:
        backup_contents = f.read()

    with open(backup_path, "w", encoding="UTF-8") as f:
        f.write(backup_contents)

    return backup_path


def rollback_requirement(backup_file, location=Path.cwd()):

    current_path = get_destination_path(location)
    requirements_path = current_path / REQUIREMENTS
    os.remove(requirements_path)

    with open(backup_file, "r", encoding="UTF-8") as f:
        backup_contents = f.read()

    with open(requirements_path, "w", encoding="UTF-8") as f:
        f.write(backup_contents)


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


def mark_notebooks_as_readonly(location: Path):

    if platform.system() == "Windows":
        execute_and_log(f'attrib +r "{location / "*.ipynb"}" /s')
    else:
        execute_and_log(f'chmod -R 0444 "{location}"/*.ipynb')


# RC FILE

def get_rc_file(folder=Path.cwd()):
    """
    Updates the needed options inside the .labskitrc file.
    """
    path = folder / GRYPHON_HISTORY
    if path.is_file():
        return path

    with open(path, "w", encoding="utf-8") as f:
        f.write("{}")

    return path


def log_new_files(template, performed_action: str, logfile=None):

    assert performed_action in [INIT, GENERATE]
    if logfile is None:
        logfile = Path.cwd() / GRYPHON_HISTORY

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
        logfile = Path.cwd() / GRYPHON_HISTORY

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


def log_add_library(libraries: list, logfile=None):

    if logfile is None:
        logfile = Path.cwd() / GRYPHON_HISTORY
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
        logger.warning("The .gryphon_history file was not found, therefore you are not inside a "
                       "Gryphon project directory.")


def get_current_python_version():
    with open(CONFIG_FILE, "r", encoding="UTF-8") as f:
        return json.load(f).get(
            "default_python_version",
            DEFAULT_PYTHON_VERSION
        )


def get_current_template_version_policy():
    with open(CONFIG_FILE, "r", encoding="UTF-8") as f:
        return json.load(f).get(
            "template_version_policy",
            USE_LATEST
        )


# TEMPLATE DOWNLOAD

def download_template(template) -> Path:
    # TODO: This implementation doesn't address cases where one template depends
    #  on another from a different index

    temp_folder = Path().cwd() / ".temp"
    status_code, _ = execute_and_log(
        f"pip --disable-pip-version-check download {template.name}"
        f"{f'=={template.version}' if hasattr(template, 'version') else ''} "
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
    if not target_folder.is_dir():
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
            dst=destination_folder,
            dirs_exist_ok=True
        )
    return destination_folder


# VERSION

def sort_versions(versions: list) -> list:
    versions.sort(key=lambda x: StrictVersion(x[1:]) if x[0] == 'v' else StrictVersion(x))
    return versions
