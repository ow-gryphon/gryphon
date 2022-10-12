import logging
import os
from pathlib import Path

from ..functions import erase_lines, BackSignal
from ..init_from_existing import init_from_existing
from ..questions import InitQuestions
from ...constants import SUCCESS, BACK
from ...fsm import State, Transition, HaltSignal
from ...fsm import negate_condition

logger = logging.getLogger('gryphon')


def _condition_ask_location_again(context: dict) -> bool:
    return "ask_location_again" in context


def _callback_ask_location_again(context: dict) -> dict:
    erase_lines(n_lines=1)
    del context["ask_location_again"]
    return context


class DealWithExistingFolder(State):

    name = "deal_with_existing_folder"

    transitions = [
        Transition(
            next_state="select_addons",
            condition=negate_condition(_condition_ask_location_again)
        ),
        Transition(
            next_state="ask_location_again",
            condition=_condition_ask_location_again,
            callback=_callback_ask_location_again
        )
    ]

    def __init__(self, registry):
        self.registry = registry

    def on_start(self, context: dict) -> dict:
        path = Path.cwd() / context["location"]
        context["n_lines_warning"] = 2

        def is_empty(x):
            return not os.listdir(x)

        if is_empty(path):
            # empty
            logger.warning("\nWARNING: The selected folder already exists.")
        else:
            # not empty
            logger.warning("\nWARNING: The selected folder is not empty.")
            want_to_go_to_init_from_existing = InitQuestions.ask_init_from_existing()

            if want_to_go_to_init_from_existing:
                ask_again = context["n_lines_ask_again"] if "n_lines_ask_again" in context else 0
                erase_lines(n_lines=context["n_lines_warning"] + ask_again)

                logger.log(SUCCESS, "Creating Gryphon project from the existing folder")
                result = init_from_existing(None, self.registry)

                if result == BACK:
                    raise BackSignal()
                else:
                    raise HaltSignal()

            else:
                # Ask location again
                context["ask_location_again"] = True
                erase_lines(n_lines=3)

        return context
