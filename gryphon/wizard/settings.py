import json
import logging
from .settings_states import (
    AskOption, PerformAction, ChangePythonVersion,
    NewTemplate, ChangeEnvManager, RestoreDefaults,
    RestoreDefaultRegistry, AddRemoteRegistry,
    AddLocalRegistry, RemoveRegistry, UpdateConda,
    ChangeTemplateVersionPolicy
)
from .functions import erase_lines, BackSignal
from ..fsm import Machine, HaltSignal
from ..constants import (
    CONFIG_FILE, DEFAULT_ENV, NAME, VALUE, BACK
)


logger = logging.getLogger('gryphon')


def back_to_previous(history, **kwargs):
    history.pop()
    erase_lines(**kwargs)


def handle_current_env_manager(tree_level):
    with open(CONFIG_FILE, "r", encoding="UTF-8") as f:
        current_env = json.load(f).get("environment_management", DEFAULT_ENV)

    response = []
    for p in tree_level:
        p = p.copy()
        name = p.pop(NAME)
        entry = dict(
            name=f"{name} (current)" if p[VALUE].lower() == current_env else name,
            **p
        )
        response.append(entry)
    return response


def settings(data_path, _):
    """Shows some configurations for power users."""

    ask_option = AskOption(data_path)

    possible_states = [
        ask_option, PerformAction(), ChangePythonVersion(),
        NewTemplate(), ChangeEnvManager(), RestoreDefaults(),
        RestoreDefaultRegistry(), AddRemoteRegistry(),
        AddLocalRegistry(), RemoveRegistry(), UpdateConda(),
        ChangeTemplateVersionPolicy()
    ]

    machine = Machine(
        initial_state=ask_option,
        possible_states=possible_states
    )

    try:
        machine.run()
    except BackSignal:
        return BACK
    except HaltSignal:
        return
