"""
File containing operations that are common to the commands.
"""
import glob
import logging
import os
import platform
import shutil
import zipfile
import datetime
import difflib
from distutils.version import StrictVersion
from pathlib import Path
from urllib.parse import urljoin

import git
import json

from .operations import BashUtils, PathUtils
from ..constants import REQUIREMENTS, CONFIG_FILE

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

    BashUtils.execute_and_log(f'cd {str(repository)} {pipe} git add . {pipe} git commit -m "Initial commit"')


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
def check_for_ssh(template):
    ssh_prefix = ""
    with open(CONFIG_FILE, "r", encoding="UTF-8") as f:
        settings_file = json.load(f)
    
    repo_url = template.repo_url
    if repo_url is not None:
        # Check if any repos require ssh-agent
        ssh_domains = settings_file.get("ssh_domains")
        
        if ssh_domains is not None:
            for ssh_domain in ssh_domains.keys():
                if ssh_domain in repo_url: # TODO: More precise check
                    if platform.system() == "Windows":
                        ssh_prefix = "start-ssh-agent & "
                    else:
                        ssh_prefix = "eval $(ssh-agent) && "
                    
    return ssh_prefix



def _download_template(template, temp_folder=Path().cwd() / ".temp"):
    """
    Downloads a template and its dependencies in the zip format to a temporary folder.
    """
    # TODO: This implementation doesn't address cases where one template depends
    #  on another from a different index

    status_code, _ = BashUtils.execute_and_log(
        f"{check_for_ssh(template)}pip --disable-pip-version-check download {template.name}"
        f"{f'=={template.version}' if hasattr(template, 'version') else ''} "
        f"-i {template.template_index} "
        f"-d \"{temp_folder}\" "
        f"--trusted-host ow-gryphon.github.io "  # TODO: Find a definitive solution for this
        f"-qqq", use_subprocess=True
    )

    # On some installations on Unix systems, only pip3 is available
    if status_code==127:
        status_code, _ = BashUtils.execute_and_log(
            f"{check_for_ssh(template)}pip3 --disable-pip-version-check download {template.name}"
            f"{f'=={template.version}' if hasattr(template, 'version') else ''} "
            f"-i {template.template_index} "
            f"-d \"{temp_folder}\" "
            f"--trusted-host ow-gryphon.github.io "  # TODO: Find a definitive solution for this
            f"-qqq", use_subprocess=True
        )

    if status_code is not None:
        raise RuntimeError(f"Unable to pip download the repository. Status code: {status_code}")


def _basic_download_template(template, temp_folder=Path().cwd() / ".temp"):
    """
    Downloads a template and its dependencies in the zip format to a temporary folder.
    """
    
    repo_url = template.repo_url
    
    if repo_url is None:
        raise RuntimeError("Metadata.json files does not contain a repo_url")
    
    # tag_url = urljoin(base_url, f"archive/refs/tags/{template.version}.zip")
    
    handler = list(filter(lambda x: x.name == "console", logger.handlers))[0]
    if handler.level > 10: 
        quiet = "--quiet"
    else:
        quiet = ""
    
    logger.info("Downloading the repository")
    
    version = template.version
    
    if version != "":
        version_string = f"--branch {version} -c advice.detachedHead=false"
    else:
        version_string = ""
    
    status_code, _ = BashUtils.execute_and_log(
        f"{check_for_ssh(template)}git clone {repo_url} \"{str(temp_folder).strip()}\" --depth 1 {quiet} {version_string}", use_subprocess=True
    )
    if status_code is not None:
        raise RuntimeError(f"Unable to git clone the repository. Status code {status_code}")
        
    # Check if .git folder is included
    git_folder = os.path.join(temp_folder, ".git")
    
    if os.path.exists(git_folder):
        clean_readonly_folder(git_folder) 


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


def _unify_templates(origin_folder: Path, destination_folder: Path, subfolder = "template") -> Path:
    """
    Copies the template and its dependencies to a single folder.
    """
    expanded_folders = glob.glob(str(origin_folder / "*"))

    for folder in expanded_folders:
    
        if subfolder is not None:
            source_folder = Path(folder) / subfolder
        else:
            source_folder = Path(folder)
            
        shutil.copytree(
            src=source_folder,
            dst=destination_folder,
            dirs_exist_ok=True
        )
    return destination_folder


def _find_matching_files(origin_folder: Path, destination_folder: Path, exclude_extensions=[]) -> tuple:
    """
    Compare the files within two folders to identify files with the same relative filepaths but different content. Return a list of those file paths.
    """
    
    # Get file paths from origin folder
    origin_file_list = []
    for root, dirs, files in os.walk(origin_folder):
        for file in files:
            file_path = os.path.join(root, file)
            origin_file_list.append(os.path.relpath(file_path, origin_folder))
    
    # Get file paths from origin folder
    shared_files = []
    for root, dirs, files in os.walk(destination_folder):
        for file in files:
            file_path = os.path.join(root, file)
            file_rel_path = os.path.relpath(file_path, destination_folder)
    
            # Check if this file exists in the origin folder
            if file_rel_path in origin_file_list:
                
                # Check if file is in list of extensions to be excluded (i.e. overwritten instead of renamed)
                if len(exclude_extensions) and _has_specific_extension(file_rel_path, exclude_extensions):
                    continue
                    
                # Check for differences between text
                try:
                    with open(origin_folder / file_rel_path, 'r') as file:
                        new_file_contents = file.read().replace('\r\n', '\n')
                except UnicodeDecodeError:
                    with open(origin_folder / file_rel_path, 'r', encoding='utf8') as file:
                        new_file_contents = file.read().replace('\r\n', '\n')

                try:
                    with open(destination_folder / file_rel_path, 'r') as file:
                        prior_file_contents = file.read().replace('\r\n', '\n')
                except UnicodeDecodeError:
                    with open(destination_folder / file_rel_path, 'r', encoding='utf8') as file:
                        prior_file_contents = file.read().replace('\r\n', '\n')
                
                if new_file_contents != prior_file_contents:
                    shared_files.append(file_rel_path)
                
    return shared_files


def _has_specific_extension(file_name, extensions):
    """Check if file_name has one of the extensions in the extensions list."""
    _, file_extension = os.path.splitext(file_name)
    return file_extension.lower() in extensions

def _rename_files(folder, files, suffix) -> tuple:
    
    copied_files = []
    
    try:
        for file in files:
            file_to_copy = folder / file
            file_path, file_ext = os.path.splitext(file_to_copy )
            new_file_name = str(file_path) + str(suffix) + str(file_ext)
            
            shutil.copy(file_to_copy, new_file_name)
            copied_files.append(new_file_name)
        
    except Exception as e:
        logger.error(f"Failed to backup files to be overwritten. Will revert changes. Full message: {str(e)}")
        
        return 1, copied_files
        
    return 0, copied_files


def backup_files_to_be_overwritten(origin_folder: Path, destination_folder: Path, subfolders, exclude_extensions=[]):
    
    suffix = datetime.datetime.now().strftime("_%Y%m%d %H%M")
    all_renamed_files = [] # List to hold full path of all files renamed
    
    for folder in subfolders:
        
        # Check if folder exists
        if not (os.path.exists(origin_folder / folder) and os.path.exists(destination_folder / folder)):
            continue
        
        # Find files
        matched_files = _find_matching_files(origin_folder / folder, destination_folder / folder, exclude_extensions)

        # Rename files by copying the existing file
        rename_error, renamed_files = _rename_files(destination_folder / folder, matched_files, suffix)
        all_renamed_files.extend([destination_folder / folder / file for file in renamed_files])
        
        if rename_error:
            _remove_files(all_renamed_files)
            raise IOError(f"Unable to back up files to be overwritten in the folder {destination_folder / folder}. ")
            
    return all_renamed_files, suffix


def log_changes(destination_folder, renamed_files, suffix):
    """
    Create a log describing all changes
    """
    
    # If no files to rename
    if len(renamed_files) == 0:
        return 0
    
    # Log outputs
    log_file_name = destination_folder / f".gryphon_warning{suffix}.txt"
    log_folder = destination_folder / f".gryphon_logs/changes{suffix}"
    
    # Create the log folder
    os.makedirs(log_folder, mode = 0o777, exist_ok = True)

    for file in renamed_files:
        
        if not _has_specific_extension(file, extensions = [".py"]):
            continue
        
        new_file = str(file).replace(suffix, "")
        
        # Compare both files using difflib
        try:
            with open(file, 'r') as file_input, open(new_file, 'r') as new_file_input:
                file_contents = file_input.read().replace('\r\n', '\n').splitlines()
                new_file_contents = new_file_input.read().replace('\r\n', '\n').splitlines()
        except: 
            with open(file, 'r', encoding='utf8') as file_input, open(new_file, 'r', encoding='utf8') as new_file_input:
                file_contents = file_input.read().replace('\r\n', '\n').splitlines()
                new_file_contents = new_file_input.read().replace('\r\n', '\n').splitlines()
        
            
        diff_html = difflib.HtmlDiff(wrapcolumn = 100).make_file(file_contents, new_file_contents, context=True)
        
        output_file = log_folder / str(os.path.relpath(new_file, destination_folder))
        output_file, _ = os.path.splitext(output_file)
        output_file = str(output_file) + ".html"
        
        os.makedirs(os.path.dirname(output_file), mode = 0o777, exist_ok = True)
        Path(output_file).write_text(diff_html)
        
    # Create the log file
    with open(log_file_name, 'w') as log_file:
        log_file.write("The following files in your project folder were backed up before being overwritten by the Gryphon template downloaded at this time: \n")
        
        for file in renamed_files:
            relative_file_path = str(os.path.relpath(file, destination_folder))
            log_file.write(f" - {relative_file_path}\n")
            
        log_file.write(f"\nFor any changed .py scripts, you can find a 'code comparison' in the \".gryphon_logs/changes{suffix}\" folder. If you want to keep your old files, rename them back. Once you are done, you can delete this file and the .gryphon_logs folder.")
    
# NOT IMPLEMENTED. NOT NEEDED CURRENTLY
#def scrub_files(folder: Path, folder_pattern = ["__pycache__", ".ipynb_checkpoints"], file_pattern = [""]):
#    """
#    Remove files from origin folder that follows a particular pattern
#    """
    

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
        shutil.rmtree(download_folder, ignore_errors=True)   # UNCOMMENT
        shutil.rmtree(zip_folder, ignore_errors=True)  # UNCOMMENT
        pass
    return template_folder
    
    
def _remove_files(files_to_remove):
    
    for file in files_to_remove:
        
        try:
            os.remove(file)
        except:
            if platform.system() == "Windows":
                BashUtils.execute_and_log(f"del /f /q \"{file}\"")
            else:
                BashUtils.execute_and_log(f"rm -f \"{file}\"")
    
#def download_template(template, project_folder):
#    download_folder = project_folder / ".temp"
#    template_folder = project_folder / ".target"
#
#    try:
#        _basic_download_template(template, download_folder)
#        shutil.copytree(
#            src=download_folder,
#            dst=template_folder,
#            dirs_exist_ok=True
#        )
#        
#    finally:
#        # shutil.rmtree(download_folder, ignore_errors=True)
#        logger.info("HERE")
#
#    return template_folder

   
def download_template(template, project_folder):
    template_folder = project_folder / ".target"

    _basic_download_template(template, template_folder)
        
    return template_folder



def clean_readonly_folder(folder):
    """
    Logic to remove folders with readonly files.
    """
    if platform.system() == "Windows":
        BashUtils.execute_and_log(f"rmdir /s /Q \"{folder}\"")
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
        "pipenv_venv" not in f and
        ".ipynb_checkpoints" not in f
    ]

