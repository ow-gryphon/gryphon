import logging

from ..functions import erase_lines
from ..questions import InitQuestions
from ...constants import BACK
from ...fsm import State, Transition, negate_condition

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

    def on_start(self, context: dict) -> dict:
        context["selected_addons"] = InitQuestions.ask_addons()
        return context

# OK: Pass witch addons were selected to the core function
# OK: Implement logic to supress addons at the time of project init
# TODO: Implement nbstripout
# TODO: Implement the same logic in the project scaffold creation
# OK: register addons on gryphon RC

# OK: define default set of addons to have as default
# OK: ADD info in the confirmation about the addons
# TODO: refactor tests to match the new user flow
