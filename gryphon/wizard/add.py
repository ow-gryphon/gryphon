import logging

from .add_states import (
    AskOption, LibraryChosen, Confirmation, AddLibrary,
    TypeLibraryName
)
from .functions import BackSignal
from ..constants import BACK
from ..fsm import Machine, HaltSignal

logger = logging.getLogger('gryphon')


def add(data_path, _):
    """add templates based on arguments and configurations."""

    ask_option = AskOption(data_path)
    library_chosen = LibraryChosen()
    confirmation = Confirmation()
    add_library = AddLibrary()
    type_library_name = TypeLibraryName()

    possible_states = [
        ask_option, library_chosen, confirmation, add_library, type_library_name
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

# TODO: Check which env manager we have on the folder
#  in order to install on the right one
