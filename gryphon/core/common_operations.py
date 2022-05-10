"""
File containing operations that are common to the commands.
"""
import glob
import json
import logging
import os
import platform
import shutil
import zipfile
from datetime import datetime
from distutils.version import StrictVersion
from pathlib import Path

import git

from .operations.bash_utils import BashUtils
from .operations.path_utils import PathUtils
from ..constants import (
    GENERATE, INIT, CONFIG_FILE, DEFAULT_PYTHON_VERSION,
    USE_LATEST
)

logger = logging.getLogger('gryphon')

REQUIREMENTS = "requirements.txt"
GRYPHON_HISTORY = ".gryphon_history"


# GIT

def init_new_git_repo(folder: Path) -> git.Repo:
    """Init new git repository on folder."""
    return git.Repo.init(folder)


def initial_git_commit(repository: git.Repo):
    """Does the first git commit."""
    repository.git.add(A=True)
    repository.index.commit("Initial commit")


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
    current_path = PathUtils.get_destination_path(location)
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

    current_path = PathUtils.get_destination_path(cwd)
    requirements_path = current_path / REQUIREMENTS
    backup_path = current_path / "requirements.backup"

    with open(requirements_path, "r", encoding="UTF-8") as f:
        backup_contents = f.read()

    with open(backup_path, "w", encoding="UTF-8") as f:
        f.write(backup_contents)

    return backup_path


def rollback_requirement(backup_file, location=Path.cwd()):

    current_path = PathUtils.get_destination_path(location)
    requirements_path = current_path / REQUIREMENTS
    os.remove(requirements_path)

    with open(backup_file, "r", encoding="UTF-8") as f:
        backup_contents = f.read()

    with open(requirements_path, "w", encoding="UTF-8") as f:
        f.write(backup_contents)


def rollback_append_requirement(library_name):
    current_path = PathUtils.get_destination_path()
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

def download_template(template, temp_folder=Path().cwd() / ".temp"):
    # TODO: This implementation doesn't address cases where one template depends
    #  on another from a different index

    status_code, _ = BashUtils.execute_and_log(
        f"pip --disable-pip-version-check download {template.name}"
        f"{f'=={template.version}' if hasattr(template, 'version') else ''} "
        f"-i {template.template_index} "
        f"-d \"{temp_folder}\" "
        f"--trusted-host ow-gryphon.github.io"  # TODO: Find a definitive solution for this
    )
    if status_code is not None:
        raise RuntimeError("Not able to find the pip command in the environment (required for this feature).")


def unzip_templates(origin_path: Path, target_folder) -> Path:
    zip_files = glob.glob(str(origin_path / "*.zip"))

    if not target_folder.is_dir():
        os.makedirs(target_folder)

    for file in zip_files:
        with zipfile.ZipFile(file, 'r') as zip_ref:
            zip_ref.extractall(target_folder)
    return target_folder


def unify_templates(origin_folder: Path, destination_folder: Path) -> Path:
    expanded_folders = glob.glob(str(origin_folder / "*"))

    for folder in expanded_folders:
        shutil.copytree(
            src=Path(folder) / "template",
            dst=destination_folder,
            dirs_exist_ok=True
        )
    return destination_folder


def clean_temporary_folders(download_folder, zip_folder, template_folder):
    shutil.rmtree(download_folder, ignore_errors=True)
    shutil.rmtree(zip_folder, ignore_errors=True)
    if platform.system() == "Windows":
        BashUtils.execute_and_log(f"rmdir /s /Q {template_folder}")
    else:
        shutil.rmtree(template_folder, ignore_errors=True)


def enable_files_overwrite(source_folder: Path, destination_folder: Path):
    pattern = "*.ipynb"

    # Get all relevant files from source
    files_to_modify = [s[s.find('notebooks'):][10:] for s in glob.glob(str(source_folder / pattern))]

    # Apply chmod to these files if they exist in the to_folder
    for target_file in files_to_modify:
        target_file_path = destination_folder / target_file
        if target_file_path.is_file():
            os.chmod(target_file_path, 0o0777)


def mark_notebooks_as_readonly(location: Path):

    if platform.system() == "Windows":
        BashUtils.execute_and_log(f'attrib +r "{location / "*.ipynb"}" /s')
    else:
        BashUtils.execute_and_log(f'chmod -R 0444 "{location}"/*.ipynb')


# VERSION

def sort_versions(versions: list) -> list:
    versions.sort(key=lambda x: StrictVersion(x[1:]) if x[0] == 'v' else StrictVersion(x))
    return versions
