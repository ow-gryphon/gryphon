from ..functions import erase_lines
from ..questions import InitQuestions
from ...fsm import State, Transition


class AskLocationAgain(State):
    name = "ask_location_again"
    transitions = [
        Transition(
            next_state="confirmation",
            condition=lambda context: True
        )
    ]

    def on_start(self, context: dict) -> dict:
        n_lines = context["n_lines"]
        erase_lines(n_lines=n_lines + 1)

        context["location"] = InitQuestions.ask_init_location()

        return context
