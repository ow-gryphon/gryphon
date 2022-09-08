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


def _go_back_callback(context: dict) -> dict:
    erase_lines(n_lines=2)
    return context


def _go_back(context: dict) -> bool:
    return context["selected_addons"] == BACK


class SelectAddons(State):

    name = "select_addons"

    transitions = [
        Transition(
            next_state="ask_parameters",
            condition=_go_back,
            callback=_go_back_callback
        ),
        Transition(
            next_state="confirmation",
            condition=negate_condition(_go_back)
        )
    ]

    def __init__(self, registry):
        self.registry = registry

    def on_start(self, context: dict) -> dict:

        location = context["location"]
        context["n_lines_warning"] = 0

        path = Path.cwd() / location

        if path.is_dir():
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
                    erase_lines(n_lines=3)

        context["selected_addons"] = InitQuestions.ask_addons()
        return context

# TODO: Implement the same logic in the project scaffold creation
# TODO: refactor tests to match the new user flow
