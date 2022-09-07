"""
File containing operations that are common to the commands.
"""
import glob
import logging
import os
import platform
import shutil
import zipfile
from distutils.version import StrictVersion
from pathlib import Path

import git

from .operations import BashUtils, PathUtils
from ..constants import REQUIREMENTS

logger = logging.getLogger('gryphon')


# GIT

def init_new_git_repo(folder: Path) -> git.Repo:
    """Init new git repository on folder."""
    return git.Repo.init(folder)


def initial_git_commit(repository: git.Repo):
    """Does the first git commit."""
    repository.git.add(A=True)
    repository.index.commit("Initial commit")


def initial_git_commit_os(repository: Path):
    """Does the first git commit."""

    pipe = "&&"
    if platform.system() == "Windows":
        pipe = "&"

    BashUtils.execute_and_log(f"cd {str(repository)} {pipe} git add . {pipe} git commit -m 'Initial commit'")


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
    """
    Appends a given requirement to the requirements.txt file.
    It checks if the library is already present in the requirements.txt folder
    before adding it or updating version number.
    """

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
    """
    Creates a copy of the requirements.txt to prevent
    losses if something goes wrong in the process.
    """
    current_path = PathUtils.get_destination_path(cwd)
    requirements_path = current_path / REQUIREMENTS
    backup_path = current_path / "requirements.backup"

    with open(requirements_path, "r", encoding="UTF-8") as f:
        backup_contents = f.read()

    with open(backup_path, "w", encoding="UTF-8") as f:
        f.write(backup_contents)

    return backup_path


def rollback_requirement(backup_file, location=Path.cwd()):
    """
    Restores the requirement.txt file.
    """
    current_path = PathUtils.get_destination_path(location)
    requirements_path = current_path / REQUIREMENTS
    os.remove(requirements_path)

    with open(backup_file, "r", encoding="UTF-8") as f:
        backup_contents = f.read()

    with open(requirements_path, "w", encoding="UTF-8") as f:
        f.write(backup_contents)


# TEMPLATE DOWNLOAD

def _download_template(template, temp_folder=Path().cwd() / ".temp"):
    """
    Downloads a template and its dependencies in the zip format to a temporary folder.
    """
    # TODO: This implementation doesn't address cases where one template depends
    #  on another from a different index

    status_code, _ = BashUtils.execute_and_log(
        f"pip --disable-pip-version-check download {template.name}"
        f"{f'=={template.version}' if hasattr(template, 'version') else ''} "
        f"-i {template.template_index} "
        f"-d \"{temp_folder}\" "
        f"--trusted-host ow-gryphon.github.io "  # TODO: Find a definitive solution for this
        f"-qqq"
    )
    if status_code is not None:
        raise RuntimeError("Not able to find the pip command in the environment (required for this feature).")


def _unzip_templates(origin_path: Path, target_folder) -> Path:
    """
    Unzips zip files contained in a given folder.
    """
    zip_files = glob.glob(str(origin_path / "*.zip"))

    if not target_folder.is_dir():
        os.makedirs(target_folder)

    for file in zip_files:
        with zipfile.ZipFile(file, 'r') as zip_ref:
            zip_ref.extractall(target_folder)
    return target_folder


def _unify_templates(origin_folder: Path, destination_folder: Path) -> Path:
    """
    Copies the template and its dependencies to a single folder.
    """
    expanded_folders = glob.glob(str(origin_folder / "*"))

    for folder in expanded_folders:
        shutil.copytree(
            src=Path(folder) / "template",
            dst=destination_folder,
            dirs_exist_ok=True
        )
    return destination_folder


def fetch_template(template, project_folder):
    download_folder = project_folder / ".temp"
    zip_folder = project_folder / ".unzip"
    template_folder = project_folder / ".target"

    try:
        _download_template(template, download_folder)
        _unzip_templates(download_folder, zip_folder)

        enable_files_overwrite(
            source_folder=zip_folder / "notebooks",
            destination_folder=template_folder / "notebooks"
        )
        _unify_templates(zip_folder, template_folder)
    finally:
        shutil.rmtree(download_folder, ignore_errors=True)
        shutil.rmtree(zip_folder, ignore_errors=True)

    return template_folder


def clean_readonly_folder(folder):
    """
    Logic to remove folders with readonly files.
    """
    if platform.system() == "Windows":
        BashUtils.execute_and_log(f"rmdir /s /Q {folder}")
    else:
        shutil.rmtree(folder, ignore_errors=True)


def enable_files_overwrite(source_folder: Path, destination_folder: Path):
    """
    Changes permissions from read only files in order to make then overridable.
    """

    # Get all relevant files from source
    files_to_modify = [
        Path(s).relative_to(source_folder)
        for s in glob.glob(str(source_folder / "**" / "*.ipynb"), recursive=True)
    ]

    # Apply chmod to these files if they exist in the to_folder
    for target_file in files_to_modify:
        target_file_path = destination_folder / target_file
        if target_file_path.is_file():
            os.chmod(target_file_path, 0o0777)


def mark_notebooks_as_readonly(location: Path):
    """
    Changes permissions from the notebooks folder in order to make it's ipython notebooks read-only.
    """
    if platform.system() == "Windows":
        BashUtils.execute_and_log(f'attrib +r "{location / "*.ipynb"}" /s')
    else:
        BashUtils.execute_and_log(f'chmod -R 0444 "{location}"/*.ipynb')


# VERSION

def sort_versions(versions: list) -> list:
    """
    Sorts a list of versions according to the semantic versioning scheme.
    """
    versions.sort(key=lambda x: StrictVersion(x[1:]) if x[0] == 'v' else StrictVersion(x))
    return versions


def multiple_file_types(*patterns):
    files = []
    for pattern in patterns:
        files.extend(glob.glob(pattern, recursive=True))

    return list(set(files))


def list_files(path: Path):
    pattern = str(path / "**" / '**')
    pattern2 = str(path / "**" / '.**')

    all_files = multiple_file_types(pattern, pattern2)

    return [
        # f.split(base_path)[1][1:]
        Path(f).relative_to(path)
        for f in all_files
        if Path(f).is_file() and
        ".git" not in f and
        "__pycache__" not in f and
        ".github" not in f and
        ".venv" not in f and
        "envs" not in f and
        ".ipynb_checkpoints" not in f
    ]
