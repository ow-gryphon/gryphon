from ..functions import erase_lines
from ..questions import SettingsQuestions
from ...constants import BACK
from ...fsm import State, Transition, negate_condition


#####
def _condition_back(context: dict) -> bool:
    return context["selected_addons"] == BACK


def _callback_back(context: dict) -> dict:
    erase_lines(n_lines=2)
    context["history"] = []
    return context


class NewTemplate2(State):
    name = "new_template2"
    transitions = [
        Transition(
            next_state="new_template3",
            condition=negate_condition(_condition_back),
        ),
        Transition(
            # CTRL + C
            next_state="new_template",
            condition=_condition_back,
            callback=_callback_back
        )
    ]

    def on_start(self, context: dict) -> dict:
        context["selected_addons"] = SettingsQuestions.ask_addons()
        return context
