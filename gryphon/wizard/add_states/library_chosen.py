from ..functions import filter_chosen_option
from ...constants import CHILDREN
from ...fsm import State, Transition, negate_condition


def _condition_library_chosen_to_ask_option(context: dict) -> bool:
    return CHILDREN in context["node"]


def _callback_library_chosen_to_ask_option(context: dict) -> dict:
    context["navigation_history"].append(context["chosen_option"])
    return context


def _callback_library_chosen_to_confirmation(context: dict) -> dict:
    context["chosen_option"] = [context["node"]]
    return context


class LibraryChosen(State):
    name = "library_chosen"
    transitions = [
        Transition(
            next_state="ask_option",
            condition=_condition_library_chosen_to_ask_option,
            callback=_callback_library_chosen_to_ask_option
        ),
        Transition(
            next_state="confirmation",
            condition=negate_condition(_condition_library_chosen_to_ask_option),
            callback=_callback_library_chosen_to_confirmation
        )
    ]

    def on_start(self, context: dict) -> dict:
        context["node"] = filter_chosen_option(
            context["chosen_option"],
            context["lib_tree"]
        )
        return context
