from ..functions import erase_lines
from ..questions import InitQuestions
from ...constants import BACK
from ...fsm import State, Transition, negate_condition


#####
def _condition_back(context: dict) -> bool:
    return context["location"] == BACK


def _callback_back(context: dict) -> dict:
    erase_lines(n_lines=2)
    context["history"] = []
    return context


class NewTemplate(State):
    name = "new_template"
    transitions = [
        Transition(
            # CTRL + C
            next_state="ask_option",
            condition=_condition_back,
            callback=_callback_back
        ),
        Transition(
            next_state="new_template2",
            condition=negate_condition(_condition_back),
        )
    ]

    def on_start(self, context: dict) -> dict:
        # ask for the folder
        context["location"] = InitQuestions.ask_just_location()

        return context
