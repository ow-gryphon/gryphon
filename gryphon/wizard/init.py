from .init_states import (
    AskTemplate, AskParameters, Confirmation,
    Install, MainMenu, AskLocationAgain, SelectAddons
)
from .functions import BackSignal
from ..constants import BACK
from ..fsm import Machine, HaltSignal


def init(_, registry):
    """Creates a starter repository for analytics projects."""

    ask_template = AskTemplate(registry)

    possible_states = [
        ask_template, Confirmation(), AskParameters(registry),
        Install(), MainMenu(), AskLocationAgain(), SelectAddons(registry)
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
