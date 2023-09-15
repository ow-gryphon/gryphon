from .download_states import (
    AskTemplate, Confirmation,
    Download, MainMenu, AskLocationAgain, AskParameters, ConfirmShellExec, AskProjectInfo
)
from .functions import BackSignal
from ..constants import BACK
from ..fsm import Machine, HaltSignal


def download(_, registry):
    """Creates a starter repository for analytics projects."""

    ask_template = AskTemplate(registry)

    possible_states = [
        ask_template, Confirmation(), Download(), MainMenu(), AskLocationAgain(), AskParameters(registry),
        ConfirmShellExec(), AskProjectInfo()
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
