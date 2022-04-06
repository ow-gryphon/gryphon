import json
import logging
from ..wizard_text import Text
from ..questions import GenerateQuestions, CommonQuestions
from ..functions import display_template_information, erase_lines
from ...fsm import Transition, State, negate_condition
from ...constants import NO, LATEST, USE_LATEST, ALWAYS_ASK, GENERATE, CONFIG_FILE

logger = logging.getLogger('gryphon')


def _condition_confirmation_to_install(context: dict) -> bool:
    return context["confirmation_response"] == NO


def _callback_confirmation_to_install(context: dict) -> dict:
    erase_lines(n_lines=len(context["extra_parameters"]) + 3 + context["n_lines"])
    return context


class Confirmation(State):
    name = "confirmation"
    transitions = [
        Transition(
            next_state="install",
            condition=negate_condition(_condition_confirmation_to_install)
        ),
        Transition(
            next_state="ask_template",
            condition=_condition_confirmation_to_install,
            callback=_callback_confirmation_to_install
        )
    ]

    def __init__(self, registry):
        self.templates = registry.get_templates(GENERATE)
        with open(CONFIG_FILE, "r+", encoding="utf-8") as f:
            self.settings = json.load(f)
        super().__init__()

    def on_start(self, context: dict) -> dict:
        template = context["templates"][context["template_name"]]

        if self.settings.get("template_version_policy") == USE_LATEST:
            context["template"] = template[LATEST]
        elif self.settings.get("template_version_policy") == ALWAYS_ASK:
            chosen_version = CommonQuestions.ask_template_version(template.available_versions)
            context["template"] = template[chosen_version]
        else:
            context["template"] = template

        context["n_lines"] = display_template_information(context["template"])

        if len(context["template"].arguments):
            logger.info(Text.generate_ask_extra_parameters)
            context["extra_parameters"] = GenerateQuestions.ask_extra_arguments(context["template"].arguments)
        else:
            context["extra_parameters"] = {}

        context["confirmation_response"] = GenerateQuestions.confirm_generate(
            template_name=context["template"].display_name,
            **context["extra_parameters"]
        )

        return context
