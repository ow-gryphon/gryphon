import logging
from pathlib import Path

from .common_operations import (
    init_new_git_repo, initial_git_commit,
)
from .operations import EnvironmentManagerOperations
from .operations.bash_utils import BashUtils
from .operations.settings import SettingsManager
from ..constants import (
    DATA_PATH, SUCCESS,
    INIT, CONDA, VENV, VENV_FOLDER
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
    # TODO: JOIN ALL THE requirements.txt files in one at the time of project init with more than one zip file
    #  downloaded.

    # Git
    repo = init_new_git_repo(folder=location)
    initial_git_commit(repo)

    # ENV Manager
    if env_type == VENV:            # VENV
        EnvironmentManagerOperations.create_venv(folder=location / VENV_FOLDER, python_version=python_version)
    elif env_type == CONDA:
        # CONDA
        EnvironmentManagerOperations.create_conda_env(location, python_version=python_version)
        # install_extra_nbextensions_conda(location)
    else:
        raise RuntimeError("Invalid \"environment_management\" option on gryphon_config.json file."
                           f"Should be one of {[INIT, CONDA]} but \"{env_type}\" was given.")

    SettingsManager.add_local_template(str(Path(location).absolute()))
    logger.info("Added new template into the gryphon registry. You will be able to find it inside gryphon according"
                " to the information given on metadata.json file.\n\n In order to find it on gryphon menus you will"
                " have to fill the template information inside metadata.json file (providing at least the display "
                "name and the command).")
    logger.log(SUCCESS, "Installation successful!")
