import json
from pathlib import Path

from ..functions import erase_lines
from ..questions import DownloadQuestions, CommonQuestions
from ...constants import (
    BACK, DOWNLOAD, ALWAYS_ASK, CONFIG_FILE,
    LATEST, USE_LATEST
)
from ...core.registry.versioned_template import VersionedTemplate
from ...fsm import State, Transition, negate_condition


def _change_from_ask_parameters_to_ask_template(context):
    return context["location"] == BACK


def _callback_from_ask_parameters_to_ask_template(context):
    erase_lines()
    return context


def _callback_from_ask_parameters_to_self(context):
    erase_lines(n_lines=2)
    return context


def _condition_confirmation(context):
    return context["location"] != BACK 


class AskParameters(State):

    def __init__(self, registry):
        self.templates = registry.get_templates(DOWNLOAD)
        with open(CONFIG_FILE, "r+", encoding="utf-8") as f:
            self.settings = json.load(f)
        super().__init__()

    name = "ask_parameters"
    transitions = [
        Transition(
            next_state="ask_template",
            condition=_change_from_ask_parameters_to_ask_template,
            callback=_callback_from_ask_parameters_to_ask_template
        ),
        Transition(
            next_state="confirmation",
            condition=_condition_confirmation,
        )
    ]

    def on_start(self, context: dict) -> dict:

        template = self.templates[context["template_name"]]

        if isinstance(template, VersionedTemplate):
            if self.settings.get("template_version_policy") == USE_LATEST:
                context["template"] = template[LATEST]

            elif self.settings.get("template_version_policy") == ALWAYS_ASK:
                chosen_version = CommonQuestions.ask_template_version(template.available_versions)
                context["template"] = template[chosen_version]

        else:
            context["template"] = template

        context["location"] = DownloadQuestions.ask_download_location()

        if context["location"] == BACK:
            return context

        context["extra_parameters"] = DownloadQuestions.ask_extra_arguments(
            arguments=context["template"].arguments
        )
        
        return context
