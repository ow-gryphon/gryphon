from pathlib import Path

from ..functions import erase_lines
from ..questions import DownloadQuestions
from ...constants import BACK
from ...fsm import State, Transition


def _condition_back(context):
    return context["location_temp"] == BACK


def _condition_ahead(context):
    return context["location_temp"] != BACK


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
        context["location_temp"] = DownloadQuestions.ask_download_location()

        return context
