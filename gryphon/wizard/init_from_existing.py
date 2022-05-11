from .init_states import (
    AskTemplate, AskParameters, Confirmation,
    Install, MainMenu, AskLocationAgain
)
from .functions import BackSignal
from ..constants import BACK
from ..fsm import Machine, HaltSignal


def init_from_existing(_, registry):
    pass
