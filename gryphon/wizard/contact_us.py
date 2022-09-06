from .contact_us_states import (
    AskTypeOfContact, Placeholder
)
from .functions import BackSignal
from ..constants import BACK
from ..fsm import Machine, HaltSignal


def contact_us(_, __):
    type_of_contact = AskTypeOfContact()

    possible_states = [
        type_of_contact, Placeholder()
    ]

    machine = Machine(
        initial_state=type_of_contact,
        possible_states=possible_states
    )

    try:
        machine.run()
    except BackSignal:
        return BACK
    except HaltSignal:
        return
