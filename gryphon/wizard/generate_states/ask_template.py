import logging
from ..questions import GenerateQuestions
from ..functions import erase_lines, BackSignal
from ...fsm import Transition, State, negate_condition
from ...constants import BACK

logger = logging.getLogger('gryphon')


def _condition_ask_template_to_ask_category(context: dict) -> bool:
    return context["template_name"] == BACK


def _callback_ask_template_to_ask_category(context: dict) -> dict:
    erase_lines(n_lines=2)
    if len(context["history"]) >= 1:
        context["history"].pop()
    else:
        raise BackSignal()

    return context


class AskTemplate(State):
    name = "ask_template"
    transitions = [
        Transition(
            next_state="ask_category",
            condition=_condition_ask_template_to_ask_category,
            callback=_callback_ask_template_to_ask_category
        ),
        Transition(
            next_state="confirmation",
            condition=negate_condition(_condition_ask_template_to_ask_category)
        )
    ]

    def on_start(self, context: dict) -> dict:
        context["template_name"] = GenerateQuestions.ask_which_template(context["filtered_templates"])

        return context
