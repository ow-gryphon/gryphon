import logging
import shutil
from pathlib import Path

from .functions import BackSignal
from .init_from_existing_states import (
    AskTemplate, MainMenu, AskLocation, AskPointExternal,
    AskExternalEnvPath, AskUseExisting, Install
)
from .questions import InitFromExistingQuestions
from ..constants import CONDA, VENV, YES, BACK, VENV_FOLDER, CONDA_FOLDER
from ..core.init_from_existing import check_for_environment
from ..core.init_from_existing import init_from_existing as init_from_existing_core, get_environment_manager
from ..core.operations import EnvironmentManagerOperations
from ..fsm import Machine, HaltSignal

logger = logging.getLogger('gryphon')


def point_to_external_inquire(path):

    point_to_external = InitFromExistingQuestions.ask_to_point_to_external_env()
    if point_to_external == YES:
        return InitFromExistingQuestions.ask_external_env_path()
    else:
        return path


def create_environment(path: Path, env_manager=None):
    if env_manager is None:
        env_manager = get_environment_manager()

    if env_manager == CONDA:
        return EnvironmentManagerOperations.create_conda_env(path)
    elif env_manager == VENV:
        return EnvironmentManagerOperations.create_venv(path / VENV_FOLDER)


def process_environment_wizard(location):

    use_existing_environment = None
    env_path = None
    env = get_environment_manager()
    found_conda, found_venv, conda_path, venv_path = check_for_environment(location)

    if found_conda or found_venv:
        # Ask the user if he wants to use this env
        # Premise: there will be one and only one environment inside the folder.

        if found_conda:
            use_existing_environment = InitFromExistingQuestions.confirm_use_existing_environment(CONDA)

            if use_existing_environment == YES:
                env = CONDA
                env_path = venv_path

        elif found_venv:
            use_existing_environment = InitFromExistingQuestions.confirm_use_existing_environment(VENV)

            if use_existing_environment == YES:
                env = VENV
                env_path = venv_path

        if use_existing_environment != YES:
            env_path = point_to_external_inquire(location)

    else:
        env_path = point_to_external_inquire(location)

    return env, use_existing_environment, env_path


def process_environment(location):

    env_path = None
    response = None
    env = get_environment_manager()

    found_conda, found_venv, conda_path, venv_path = check_for_environment(location)
    if found_conda or found_venv:
        # Ask the user if he wants to use this env
        # Premise: there will be one and only one environment inside the folder.
        if found_conda:
            env = CONDA
            response = InitFromExistingQuestions.confirm_use_existing_environment(CONDA)
            if response == "no_delete":
                shutil.rmtree(conda_path)

            if response == YES:
                env_path = conda_path

        elif found_venv:
            env = VENV
            response = InitFromExistingQuestions.confirm_use_existing_environment(VENV)
            if response == "no_delete":
                shutil.rmtree(venv_path)

            if response == YES:
                env_path = venv_path

        if response != YES:
            env_path = point_to_external_inquire(location)

    else:
        env_path = point_to_external_inquire(location)

    return env, env_path


def init_from_existing_(_, __):
    """
    Transforms an existing code folder into a gryphon project.
    """

    # Ask folder
    location = InitFromExistingQuestions.ask_existing_location()

    # ENVIRONMENT
    env, use_existing_environment, env_path = process_environment_wizard(location)
    print(location, env, use_existing_environment, env_path)
    init_from_existing_core(location, env, use_existing_environment, env_path)


def init_from_existing(_, registry):

    ask_template = AskTemplate(registry)

    possible_states = [
        ask_template, MainMenu(), AskLocation(), AskPointExternal(),
        AskExternalEnvPath(), AskUseExisting(), Install()

    ]

    machine = Machine(
        initial_state=ask_template,
        possible_states=possible_states
    )

    try:
        machine.run()
    except BackSignal:
        return BACK
    except HaltSignal:
        return
