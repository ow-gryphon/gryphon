from typing import List, Dict, Tuple
from ..functions import erase_lines
from ..questions import InitQuestions
from ...finite_state_machine import State, Transition


class AskLocationAgain(State):
    name = "ask_location_again"
    transitions = [
        Transition(
            next_state="confirmation",
            condition=lambda *args, **kwargs: True
        )
    ]

    def __init__(self):
        super().__init__(self.name, self.transitions)

    def on_start(self, *args, **kwargs) -> Tuple[List, Dict]:
        n_lines = kwargs["n_lines"]
        erase_lines(n_lines=n_lines + 1)

        kwargs["location"] = InitQuestions.ask_init_location()

        return list(args), dict(kwargs)
