import os
import platform
from ..functions import erase_lines
from ..questions import AddQuestions
from ...constants import YES, NO
from ...fsm import State, Transition


def _condition_confirmation_to_back(context: dict) -> bool:
    return context["confirmation_response"] == NO


def _callback_confirmation_to_back(context: dict) -> dict:
    erase_lines(n_lines=2)
    erase_lines(n_lines=context["n_lines"])
    return context


def _condition_confirmation_to_open_website(context: dict) -> bool:
    return context["confirmation_response"] not in [YES, NO]


def _callback_confirmation_open_website(context: dict) -> dict:
    response = context["confirmation_response"]
    n_lines = context["n_lines"]

    if platform.system() == "Windows":
        os.system(f"start {response}")
        erase_lines(n_lines=1)
    else:
        os.system(f"""nohup xdg-open "{response}" """)
        os.system(f"""rm nohup.out""")
        erase_lines()
    erase_lines(n_lines=n_lines)
    return context


def _condition_confirmation_to_add_library(context: dict) -> bool:
    return context["confirmation_response"] == YES


class Confirmation(State):
    name = "confirmation"
    transitions = [
        Transition(
            next_state="confirmation",
            condition=_condition_confirmation_to_open_website,
            callback=_callback_confirmation_open_website
        ),
        Transition(
            next_state="ask_option",
            condition=_condition_confirmation_to_back,
            callback=_callback_confirmation_to_back
        ),
        Transition(
            next_state="add_library",
            condition=_condition_confirmation_to_add_library
        )
    ]

    def on_start(self, context: dict) -> dict:

        context["confirmation_response"], context["n_lines"] = AddQuestions.confirm_add(context["chosen_option"])
        return context
