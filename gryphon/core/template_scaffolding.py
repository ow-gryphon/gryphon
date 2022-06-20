import logging
from pathlib import Path

from .common_operations import (
    init_new_git_repo, initial_git_commit,
)
from .operations import (
    EnvironmentManagerOperations, BashUtils,
    SettingsManager, PreCommitManager
)
from ..constants import (
    DATA_PATH, SUCCESS, REQUIREMENTS,
    INIT, CONDA, VENV, VENV_FOLDER, CONDA_FOLDER
)

logger = logging.getLogger('gryphon')


def template_scaffolding(location: Path):

    template_path = DATA_PATH / "template_scaffolding"
    location = Path(location)

    python_version = SettingsManager.get_current_python_version()
    env_type = SettingsManager.get_environment_manager()

    logger.info("Creating project scaffolding.")
    logger.info(f"Initializing project at {location}")

    # Files
    BashUtils.copy_project_template(
        template_destiny=location,
        template_source=Path(template_path)
    )

    PreCommitManager.fill_configurations(location)

    # TODO: JOIN ALL THE requirements.txt files in one at the time of project
    #  init with more than one zip file downloaded.

    # Git
    repo = init_new_git_repo(folder=location)
    initial_git_commit(repo)

    # ENV Manager
    if env_type == VENV:            # VENV
        env_folder = location / VENV_FOLDER
        env_folder = EnvironmentManagerOperations.create_venv(env_folder, python_version=python_version)
        EnvironmentManagerOperations.install_libraries_venv(
            environment_path=env_folder,
            requirements_path=location / REQUIREMENTS
        )

    elif env_type == CONDA:
        # CONDA
        env_folder = location / CONDA_FOLDER
        env_folder = EnvironmentManagerOperations.create_conda_env(env_folder, python_version=python_version)
        EnvironmentManagerOperations.install_libraries_conda(
            environment_path=env_folder,
            requirements_path=location / REQUIREMENTS
        )

    else:
        raise RuntimeError("Invalid \"environment_management\" option on gryphon_config.json file."
                           f"Should be one of {[INIT, CONDA]} but \"{env_type}\" was given.")

    # install pre-commit hooks
    PreCommitManager.install_pre_commit(env_folder, location)

    SettingsManager.add_local_template(str(Path(location).absolute()))
    logger.info("Added new template into the gryphon registry. You will be able to find it inside gryphon according"
                " to the information given on metadata.json file.\n\n In order to find it on gryphon menus you will"
                " have to fill the template information inside metadata.json file (providing at least the display "
                "name and the command).")
    logger.log(SUCCESS, "Installation successful!")

# DONE: install pre-commit hooks on init
# TODO: add .pre-commit-config.yaml on the template folders
# TODO: prompt whether the template scaffolding is for init or generate]
# TODO: way to choose which pre-commit hooks ones want to add
