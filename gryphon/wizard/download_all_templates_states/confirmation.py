import logging
import os
import platform
from pathlib import Path

from ..functions import erase_lines
from ..questions import DownloadQuestions
from ...constants import YES, NO, READ_MORE, CHANGE_LOCATION, GENERATE
from ...fsm import State, Transition

import questionary
from questionary import Choice, Separator

logger = logging.getLogger('gryphon')


def confirmation_success_callback(context: dict) -> dict:
    n_lines = context["n_lines"]
    ask_again = context["n_lines_ask_again"] if "n_lines_ask_again" in context else 0

    erase_lines(n_lines=n_lines + 2 + context["n_lines_warning"] + ask_again)
    return context


def ask_location_again_callback(context: dict) -> dict:
    n_lines = context["n_lines"]
    ask_again = context["n_lines_ask_again"] if "n_lines_ask_again" in context else 0

    erase_lines(n_lines=n_lines + 1 + context["n_lines_warning"] + ask_again)
    return context

def _change_from_confirmation_download(context: dict) -> bool:
    confirmed = context["confirmed"]
    return confirmed == YES

def _change_from_confirmation_to_ask_location_again(context: dict) -> bool:
    confirmed = context["confirmed"]
    return confirmed == CHANGE_LOCATION


class Confirmation(State):

    def __init__(self, registry):
        self.templates = registry.get_templates(GENERATE)
        
        super().__init__()

    name = "confirmation"
    transitions = [
        Transition(
            next_state="download",
            condition=_change_from_confirmation_download
        ),
        Transition(
            next_state="ask_location_again",
            condition=_change_from_confirmation_to_ask_location_again,
            callback=ask_location_again_callback
        )
    ]

    def on_start(self, context: dict) -> dict:
        
        options = [
            Choice(
                title="Yes",
                value=YES
            ),
            Choice(
                title="No",
                value=NO
            )
        ]
        
        confirmed = questionary.select(
            message=message,
            choices=options
        ).unsafe_ask()

        context.update(dict(
            n_lines=2, # n_lines,
            confirmed=confirmed
        ))

        return context
