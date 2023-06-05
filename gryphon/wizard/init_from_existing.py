import logging

from .functions import BackSignal
from .init_from_existing_states import (
    AskTemplate, MainMenu, AskLocation, AskPointExternal, AskProjectInfo,
    AskExternalEnvPath, AskUseExisting, Install
)
from ..constants import BACK
from ..fsm import Machine, HaltSignal

logger = logging.getLogger('gryphon')


def init_from_existing(_, registry):

    ask_template = AskTemplate(registry)

    possible_states = [
        ask_template, MainMenu(), AskLocation(registry), AskPointExternal(), AskProjectInfo(),
        AskExternalEnvPath(), AskUseExisting(), Install(registry)
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
