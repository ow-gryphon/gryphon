import json
from ..functions import get_current_tree_state, erase_lines, BackSignal
from ..questions import AddQuestions
from ...constants import BACK, TYPING
from ...fsm import State, Transition


def _condition_ask_option_to_add(context: dict) -> bool:
    return not len(context["lib_tree"])


def _condition_ask_option_to_previous(context: dict) -> bool:
    return context["chosen_option"] == BACK \
           and not len(context["navigation_history"]) >= 1


def _callback_ask_option_to_previous(_):
    erase_lines(n_lines=2)
    raise BackSignal()


def _condition_ask_option_to_ask_option(context: dict) -> bool:
    return context["chosen_option"] == BACK \
           and len(context["navigation_history"]) >= 1


def _callback_ask_option_to_ask_option(context: dict):
    context["navigation_history"].pop()
    erase_lines(n_lines=2)
    return context


def _condition_ask_option_to_type(context: dict) -> bool:
    return context["chosen_option"] == TYPING


def _condition_ask_option_to_library_chosen(context: dict) -> bool:
    return (
        (not _condition_ask_option_to_add(context)) and
        (not context["chosen_option"] == BACK) and
        (not _condition_ask_option_to_type(context))
    )


class AskOption(State):
    name = "ask_option"
    transitions = [
        Transition(
            next_state="add",
            condition=_condition_ask_option_to_add
        ),
        Transition(
            next_state="ask_option",
            condition=_condition_ask_option_to_previous,
            callback=_callback_ask_option_to_previous
        ),
        Transition(
            next_state="ask_option",
            condition=_condition_ask_option_to_ask_option,
            callback=_callback_ask_option_to_ask_option
        ),
        Transition(
            next_state="type_library_name",
            condition=_condition_ask_option_to_type
        ),
        Transition(
            next_state="library_chosen",
            condition=_condition_ask_option_to_library_chosen
        )
    ]

    def __init__(self, data_path):
        with open(data_path / "library_tree.json", encoding='utf-8') as file:
            self.full_tree = json.load(file)
        super().__init__()

    def on_start(self, context: dict) -> dict:
        if "navigation_history" not in context:
            context["navigation_history"] = []

        context["lib_tree"] = get_current_tree_state(
            tree=self.full_tree,
            history=context["navigation_history"]
        )

        # chosen option
        context["chosen_option"] = AddQuestions.get_add_option(context["lib_tree"])

        return context
