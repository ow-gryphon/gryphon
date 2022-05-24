from .handover_states import *
from .functions import BackSignal
from ..constants import BACK
from ..fsm import Machine, HaltSignal


def handover(_, registry):
    """Creates a starter repository for analytics projects."""

    ask_folder = AskFolder()

    possible_states = [
        ask_folder
    ]

    machine = Machine(
        initial_state=ask_folder,
        possible_states=possible_states
    )

    try:
        machine.run()
    except BackSignal:
        return BACK
    except HaltSignal:
        return
