from .init_states import (
    AskTemplate, AskParameters, Confirmation,
    Install, MainMenu, AskLocationAgain
)
from .functions import BackSignal
from ..constants import BACK
from ..fsm import Machine, HaltSignal


def init(_, registry):
    """Creates a starter repository for analytics projects."""

    ask_template = AskTemplate(registry)
    ask_parameters = AskParameters(registry)
    confirmation = Confirmation()
    install = Install()
    main_menu = MainMenu()
    ask_location_again = AskLocationAgain()

    possible_states = [
        main_menu, ask_template, confirmation, ask_parameters, install,
        ask_location_again
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
