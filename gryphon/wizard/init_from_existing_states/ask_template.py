from ..questions import InitQuestions
from ...fsm import State, Transition, negate_condition
from ...constants import INIT, BACK


def _change_from_ask_template_to_main_menu(context):
    return context["template_name"] == BACK


class AskTemplate(State):

    def __init__(self, registry):
        all_init_templates = registry.get_templates(INIT)
        
        # Filter out irrelevant templates
        relevant_templates = {}
        
        for name, template in all_init_templates.items():
            if template.force_env in ["pipenv"]:
                pass
            else:
                relevant_templates[name] = template
    
        self.templates = relevant_templates
        super().__init__()

    name = "ask_template"
    transitions = [
        Transition(
            next_state="main_menu",
            condition=_change_from_ask_template_to_main_menu
        ),
        Transition(
            next_state="ask_location",
            condition=negate_condition(_change_from_ask_template_to_main_menu)
        )
    ]

    def on_start(self, context: dict) -> dict:
        context["template_name"] = InitQuestions.ask_which_template(self.templates)
        return context
