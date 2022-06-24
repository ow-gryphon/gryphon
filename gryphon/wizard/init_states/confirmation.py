import logging
from pathlib import Path
from ..functions import erase_lines
from ..questions import InitQuestions
from ...fsm import State, Transition
from ...constants import YES, NO

logger = logging.getLogger('gryphon')


def confirmation_success_callback(context: dict) -> dict:
    n_lines = context["n_lines"]
    ask_again = context["n_lines_ask_again"] if "n_lines_ask_again" in context["n_lines_ask_again"] else 0

    erase_lines(n_lines=n_lines + 3 + context["n_lines_warning"] + ask_again)
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

        context["n_lines_warning"] = 0
        path = Path.cwd() / location
        if path.is_dir():
            context["n_lines_warning"] = 1
            logger.warning("WARNING: The selected folder already exists.")

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
