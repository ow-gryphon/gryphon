from ..questions import GenerateQuestions
from ..functions import erase_lines, BackSignal
from ...fsm import Transition, State
from ...constants import BACK, QUIT, SEARCH_BY_KEYWORD, TYPE_AGAIN


def ask_what_to_do_if_nothing_found(state: dict):

    if state["actual_selection"] == SEARCH_BY_KEYWORD:
        response = GenerateQuestions.nothing_found_typing()
    else:
        response = GenerateQuestions.nothing_found()

    if response == QUIT:
        exit(0)

    return response


def _callback_ask_keyword(context: dict) -> dict:
    erase_lines()
    return context


def _callback_ask_category(context: dict) -> dict:
    erase_lines(n_lines=2)

    if len(context["history"]) >= 1:
        context["history"].pop()
    else:
        raise BackSignal()

    return context


class NothingFound(State):
    name = "nothing_found"
    transitions = [
        Transition(
            next_state="ask_keyword",
            condition=lambda context: context["what_to_do"] == TYPE_AGAIN,
            callback=_callback_ask_keyword
        ),
        Transition(
            next_state="ask_category",
            condition=lambda context: context["what_to_do"] == BACK,
            callback=_callback_ask_category
        )
    ]

    def on_start(self, context: dict) -> dict:
        context["what_to_do"] = ask_what_to_do_if_nothing_found(context)

        return context
