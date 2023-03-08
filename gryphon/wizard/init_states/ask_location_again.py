from pathlib import Path

from ..functions import erase_lines
from ..questions import InitQuestions
from ...constants import BACK
from ...fsm import State, Transition


def _condition_back(context):
    return context["location_temp"] == BACK


def _condition_ahead(context):
    return context["location_temp"] != BACK and "selected_addons" in context


def _condition_deal_existing(context):
    return context["location_temp"] != BACK and "selected_addons" not in context and \
           (Path.cwd() / context["location_temp"]).is_dir()


def _condition_select_addons(context):
    return context["location_temp"] != BACK and "selected_addons" not in context and \
           not ((Path.cwd() / context["location_temp"]).is_dir())


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
            next_state="deal_with_existing_folder",
            condition=_condition_deal_existing,
            callback=_callback_ahead
        ),
        Transition(
            next_state="select_addons",
            condition=_condition_select_addons,
            callback=_callback_ahead
        ),
        Transition(
            next_state="confirmation",
            condition=_condition_ahead,
            callback=_callback_ahead
        ),
        Transition(
            next_state="confirmation",
            condition=_condition_back,
            callback=_callback_back
        )
    ]

    def on_start(self, context: dict) -> dict:
        context["location_temp"] = str(InitQuestions.ask_init_location()).strip()

        return context
