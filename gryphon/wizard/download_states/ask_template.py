from ..questions import DownloadQuestions
from ...fsm import State, Transition, negate_condition
from ...constants import DOWNLOAD, BACK


def _change_from_ask_template_to_main_menu(context):
    return context["template_name"] == BACK


class AskTemplate(State):

    def __init__(self, registry):
        self.templates = registry.get_templates(DOWNLOAD)
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
        context["template_name"] = DownloadQuestions.ask_which_template(self.templates)

        return context
