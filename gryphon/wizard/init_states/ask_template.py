from ..questions import InitQuestions
from ...fsm import State, Transition, negate_condition
from ...constants import INIT, BACK


def _change_from_ask_template_to_main_menu(context):
    template_name = context["template_name"]
    return template_name == BACK


class AskTemplate(State):

    def __init__(self, registry):
        self.templates = registry.get_templates(INIT)
        super().__init__()

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

    def on_start(self, context: dict) -> dict:
        template_name, location = InitQuestions.ask_which_template(self.templates)
        context.update(dict(
            template_name=template_name,
            location=location
        ))
        return context
