"""
Module containing the code for the init command in the CLI.
"""
import os
import json
import logging
from pathlib import Path
from .common_operations import (
    install_libraries,
    copy_project_template,
    create_venv,
    init_new_git_repo,
    initial_git_commit,
    populate_rc_file,
    change_shell_folder_and_activate_venv,
    get_rc_file,
    create_conda_env, conda_install_requirements
    # install_extra_nbextensions
)


logger = logging.getLogger('gryphon')
PACKAGE_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = Path(PACKAGE_PATH).parent / "data"


def init(template_path, location, **kwargs):
    """
    Init command from the OW Gryphon CLI.
    """

    with open(DATA_PATH / "gryphon_config.json") as f:
        env_type = json.load(f).get("environment_management", "venv")

    logger.info("Creating project scaffolding.")
    kwargs.copy()

    logger.info(f"Initializing project at {location}")
    copy_project_template(
        template_destiny=Path(location),
        template_source=Path(template_path)
    )

    rc_file = get_rc_file(Path.cwd() / location)
    populate_rc_file(rc_file, f"INIT {location} {template_path}")
    repo = init_new_git_repo(folder=location)
    initial_git_commit(repo)

    if env_type == "venv":
        create_venv(folder=location)
        install_libraries(folder=location)
        # install_extra_nbextensions(location)
        change_shell_folder_and_activate_venv(location)
    elif env_type == "conda":
        create_conda_env(location)
        conda_install_requirements(location)
    else:
        raise RuntimeError("Invalid \"environment_management\" option on gryphon_config.json file."
                           f"Should be one of [\"venv\", \"conda\"] but \"{env_type}\" was given.")
