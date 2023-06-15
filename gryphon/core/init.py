"""
Module containing the code for the init command in the CLI.
"""
import json
import logging
import os
import shutil
import platform
from pathlib import Path

from .common_operations import (
    init_new_git_repo, initial_git_commit,
    fetch_template, append_requirement,
    mark_notebooks_as_readonly,
    clean_readonly_folder, enable_files_overwrite,
    backup_files_to_be_overwritten, log_changes
)
from .operations import (
    BashUtils, EnvironmentManagerOperations, NBStripOutManager,
    RCManager, SettingsManager, PreCommitManager, NBExtensionsManager
)
from .registry import Template
from ..constants import (
    DEFAULT_ENV, INIT, VENV, PIPENV, CONDA, REMOTE_INDEX, SUCCESS,
    LOCAL_TEMPLATE, VENV_FOLDER, CONDA_FOLDER, REQUIREMENTS, CONFIG_FILE
)

logger = logging.getLogger('gryphon')


def handle_template(template, project_home, rc_file):
    if template.registry_type == REMOTE_INDEX:

        template_folder = fetch_template(template, project_home)
        all_renamed_files = []
        
        try:
            enable_files_overwrite(
                source_folder=template_folder / "notebooks",
                destination_folder=project_home / "notebooks"
            )
            mark_notebooks_as_readonly(template_folder / "notebooks")
            
            all_renamed_files, suffix = backup_files_to_be_overwritten(Path(template_folder), Path(project_home), subfolders = ["utilities"])
            
            # Move files to destination
            shutil.copytree(
                src=Path(template_folder),
                dst=project_home,
                dirs_exist_ok=True,
                ignore=shutil.ignore_patterns(
                    ".git",
                    ".github",
                    "__pycache__",
                    "envs",
                    ".venv",
                    ".ipynb_checkpoints"
                )
            )
            
        except Exception as e:
            logger.error("Failed to move template files into target folder.")
            logger.error(str(e))
        
        finally:
            RCManager.log_new_files(template, template_folder, performed_action=INIT, logfile=rc_file)
            clean_readonly_folder(template_folder)
            
            # Log changes to files            
            if (all_renamed_files is not None) and (len(all_renamed_files) > 0):
                log_changes(destination_folder = project_home, renamed_files = all_renamed_files, suffix = suffix)
                
                logger.info(f"The following files were overwritten and the old version has been backed up with new file names: ")
                logger.info([str(os.path.relpath(file, project_home)) for file in all_renamed_files])

    elif template.registry_type == LOCAL_TEMPLATE:

        BashUtils.copy_project_template(
            template_destiny=project_home,
            template_source=Path(template.path)  # / "template"
        )

        # RCManager.log_new_files(template, Path(template.path) / "template", performed_action=INIT, logfile=rc_file)
        RCManager.log_new_files(template, Path(template.path), performed_action=INIT, logfile=rc_file)

    else:
        raise RuntimeError(f"Invalid registry type: {template.registry_type}.")
        


def init(template: Template, location, python_version,
         install_nbextensions=False,
         install_nb_strip_out=False,
         install_pre_commit_hooks=False,
         **kwargs
         ):
    """
    Init command from the OW Gryphon CLI.
    """
    kwargs.copy()
    
    force_env = template.force_env
    
    if force_env:
        env_type = force_env
    else:
        with open(SettingsManager.get_config_path(), "r", encoding="UTF-8") as f:
            data = json.load(f)
            env_type = data.get("environment_management", DEFAULT_ENV)

    project_home = Path.cwd() / location

    logger.info(f"Initializing project at {project_home}")
    
    try:
        os.makedirs(project_home, exist_ok=True)
    except Exception as e:
        logger.error("Unable to access the folder. Please check the folder path.")
        logger.debug(str(e))
        
    # RC file
    rc_file = RCManager.get_rc_file(project_home)
    RCManager.log_operation(template, performed_action=INIT, logfile=rc_file)
    
    # TEMPLATE
    handle_template(template, project_home, rc_file)

    if install_pre_commit_hooks:
        PreCommitManager.initial_setup(project_home)

    # Git
    repo = init_new_git_repo(folder=project_home)
    # initial_git_commit_os(project_home)
    initial_git_commit(repo)

    # Requirements
    if env_type != PIPENV:
        for r in template.dependencies:
            append_requirement(r, project_home)
    else:
        pipenv_requirements = []
        pipenv_requirements.extend(template.dependencies)
        pipenv_requirements = list(set(pipenv_requirements))
        
    RCManager.log_add_library(template.dependencies, logfile=rc_file)

    # ENV Manager
    if env_type == PIPENV:
        
        with open(CONFIG_FILE, "r", encoding="UTF-8") as f:
            settings_file = json.load(f)
        use_this_folder = settings_file.get("pipenv_in_project")
        
        logger.debug(f"use folder: {use_this_folder}")
        
        if use_this_folder is None:
            use_this_folder = False
            
        EnvironmentManagerOperations.create_pipenv_venv(project_folder = project_home, current_folder=use_this_folder)
        
        RCManager.set_environment_manager(PIPENV, logfile=rc_file)
        
        if use_this_folder:
            RCManager.set_environment_manager_path("project_folder", logfile=rc_file)
        else:
            RCManager.set_environment_manager_path("default", logfile=rc_file)
            
        # Install libraries
        logger.debug(pipenv_requirements)
        
        print(pipenv_requirements)
        
        EnvironmentManagerOperations.install_libraries_pipenv(pipenv_requirements)
        
        
    elif env_type == VENV:
        # VENV
        env_path = EnvironmentManagerOperations.create_venv(
            folder=project_home / VENV_FOLDER,
            python_version=python_version
        )

        RCManager.set_environment_manager(VENV, logfile=rc_file)
        RCManager.set_environment_manager_path(env_path, logfile=rc_file)

        EnvironmentManagerOperations.install_libraries_venv(
            environment_path=project_home / VENV_FOLDER,
            requirements_path=project_home / REQUIREMENTS
        )

        if install_nbextensions:
            logger.info("Installing extra notebook extensions.")

            NBExtensionsManager.install_extra_nbextensions_venv(
                environment_path=project_home / VENV_FOLDER,
                requirements_path=project_home / REQUIREMENTS
            )
            logger.log(SUCCESS, "Notebook extensions installed successfully.")

    elif env_type == CONDA:
        # CONDA

        env_path = EnvironmentManagerOperations.create_conda_env(
            project_home / CONDA_FOLDER,
            python_version=python_version
        )

        RCManager.set_environment_manager(CONDA, logfile=rc_file)
        RCManager.set_environment_manager_path(env_path, logfile=rc_file)

        EnvironmentManagerOperations.install_libraries_conda(
            environment_path=project_home / CONDA_FOLDER,
            requirements_path=project_home / REQUIREMENTS
        )

        if install_nbextensions:
            logger.info("Installing extra notebook extensions.")
            NBExtensionsManager.install_extra_nbextensions_conda(
                environment_path=project_home / CONDA_FOLDER,
                requirements_path=project_home / REQUIREMENTS
            )
            logger.log(SUCCESS, "Notebook extensions installed successfully.")

    else:
        raise RuntimeError("Invalid \"environment_management\" option on gryphon_config.json file."
                           f"Should be one of {[INIT, CONDA]} but \"{env_type}\" was given.")

    if install_nb_strip_out:
        logger.info("Installing nbstripout")
        NBStripOutManager.setup(project_home, environment_path=env_path)
        logger.log(SUCCESS, "Nbstripout installed successfully.")

    if install_pre_commit_hooks:
        logger.info("Installing pre-commit hooks")
        PreCommitManager.final_setup(project_home)
        logger.log(SUCCESS, "Pre-commit hooks installed successfully.")

    # update addons in gryphon_rc
    RCManager.set_addon_states(
        install_nb_strip_out=install_nb_strip_out,
        install_nbextensions=install_nbextensions,
        install_pre_commit_hooks=install_pre_commit_hooks,
        logfile=rc_file
    )
    
    # Check if any shell script is provided
    if template.shell_exec is not None:
        logger.info(f"Executing additional shell script: cd \"{project_home}\" & {template.shell_exec}.")
        
        if platform.system() == "Windows":
            BashUtils.execute_and_log(f"cd \"{project_home}\" & {template.shell_exec}")
        else:
            BashUtils.execute_and_log(f"cd \"{project_home}\" && {str(template.shell_exec).replace('&','&&')}")
        
    EnvironmentManagerOperations.final_instructions(project_home, env_manager=env_type)

    logger.log(SUCCESS, "Project created successfully.")
