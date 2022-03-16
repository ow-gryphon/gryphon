from ..questions import GenerateQuestions
from ..functions import erase_lines, BackSignal
from ...fsm import Transition, State
from ...constants import BACK, QUIT


def ask_what_to_do_if_nothing_found(state: dict):
    response = GenerateQuestions.nothing_found()
    if response == QUIT:
        exit(0)

    if response == BACK:
        erase_lines(n_lines=2)

    if len(state["history"]) >= 1:
        state["history"].pop()
    else:
        raise BackSignal()


def _callback_nothing_found(context: dict) -> dict:
    ask_what_to_do_if_nothing_found(context)
    return context


class NothingFound(State):
    name = "nothing_found"
    transitions = [
        Transition(
            next_state="ask_category",
            condition=lambda context: not bool(len(context["filtered_templates"])),
            callback=_callback_nothing_found
        ),
        Transition(
            next_state="ask_template",
            condition=lambda context: bool(len(context["filtered_templates"]))
        )
    ]

    def on_start(self, context: dict) -> dict:
        return context
