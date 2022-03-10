from typing import List, Dict, Tuple
from ..questions import InitQuestions
from ...finite_state_machine import State, Transition, negate_condition
from ...constants import INIT, BACK


def _change_from_ask_template_to_main_menu(*_, **kwargs):
    template_name = kwargs["template_name"]
    return template_name == BACK


class AskTemplate(State):

    def __init__(self, registry):
        self.templates = registry.get_templates(INIT)
        super().__init__(self.name, self.transitions)

    name = "ask_template"
    transitions = [
        Transition(
            next_state="main_menu",
            condition=_change_from_ask_template_to_main_menu
        ),
        Transition(
            next_state="ask_parameters",
            condition=negate_condition(_change_from_ask_template_to_main_menu)
        )
    ]

    def on_start(self, *args, **kwargs) -> Tuple[List, Dict]:
        template_name, location = InitQuestions.ask_which_template(self.templates)
        kwargs.update(dict(
            template_name=template_name,
            location=location
        ))
        return list(args), dict(kwargs)
