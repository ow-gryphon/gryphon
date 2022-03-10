from pathlib import Path
from typing import List, Dict, Tuple
from ..functions import erase_lines
from ..questions import InitQuestions
from ...finite_state_machine import State, Transition
from ...constants import YES, NO


def confirmation_success_callback(*_, **kwargs):
    n_lines = kwargs["n_lines"]
    erase_lines(n_lines=n_lines + 2)


def _change_from_confirmation_to_install(*_, **kwargs):
    confirmed = kwargs["confirmed"]
    return confirmed == YES


def _change_from_confirmation_to_ask_template(*_, **kwargs):
    confirmed = kwargs["confirmed"]
    return confirmed == NO


def _change_from_confirmation_to_ask_location_again(*_, **kwargs):
    confirmed = kwargs["confirmed"]
    return confirmed == "change_location"


class Confirmation(State):

    def __init__(self):
        super().__init__(self.name, self.transitions)

    name = "confirmation"
    transitions = [
        Transition(
            next_state="ask_template",
            condition=_change_from_confirmation_to_ask_template,
            callback=confirmation_success_callback
        ),
        Transition(
            next_state="install",
            condition=_change_from_confirmation_to_install
        ),
        Transition(
            next_state="ask_location_again",
            condition=_change_from_confirmation_to_ask_location_again
        )
    ]

    def on_start(self, *args, **kwargs) -> Tuple[List, Dict]:
        template = kwargs["template"]
        location = kwargs["location"]
        extra_parameters = kwargs["extra_parameters"]

        confirmed, n_lines = InitQuestions.confirm_init(
            template=template,
            location=Path(location).resolve(),
            **extra_parameters
        )

        kwargs.update(dict(
            n_lines=n_lines,
            confirmed=confirmed
        ))
        return list(args), dict(kwargs)
