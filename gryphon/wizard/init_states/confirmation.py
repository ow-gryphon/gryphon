from pathlib import Path
from ..functions import erase_lines
from ..questions import InitQuestions
from ...fsm import State, Transition
from ...constants import YES, NO


def confirmation_success_callback(context: dict) -> dict:
    n_lines = context["n_lines"]
    erase_lines(n_lines=n_lines + 2)
    return context


def _change_from_confirmation_to_install(context: dict) -> bool:
    confirmed = context["confirmed"]
    return confirmed == YES


def _change_from_confirmation_to_ask_template(context: dict) -> bool:
    confirmed = context["confirmed"]
    return confirmed == NO


def _change_from_confirmation_to_ask_location_again(context: dict) -> bool:
    confirmed = context["confirmed"]
    return confirmed == "change_location"


class Confirmation(State):

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

    def on_start(self, context: dict) -> dict:
        template = context["template"]
        location = context["location"]
        extra_parameters = context["extra_parameters"]

        confirmed, n_lines = InitQuestions.confirm_init(
            template=template,
            location=Path(location).resolve(),
            **extra_parameters
        )

        context.update(dict(
            n_lines=n_lines,
            confirmed=confirmed
        ))
        return context
