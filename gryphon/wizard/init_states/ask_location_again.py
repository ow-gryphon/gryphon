from ..functions import erase_lines
from ..questions import InitQuestions
from ...constants import BACK
from ...fsm import State, Transition, negate_condition


def _condition_back(context):
    return context["location_temp"] == BACK


def _callback_back(context):
    erase_lines(n_lines=1)
    return context


def _callback_ahead(context):
    context["location"] = context["location_temp"]
    return context


class AskLocationAgain(State):
    name = "ask_location_again"
    transitions = [
        Transition(
            next_state="confirmation",
            condition=negate_condition(_condition_back),
            callback=_callback_ahead
        ),
        Transition(
            next_state="confirmation",
            condition=_condition_back,
            callback=_callback_back
        )
    ]

    def on_start(self, context: dict) -> dict:
        context["location_temp"] = InitQuestions.ask_init_location()

        return context
