import json
import logging
# import os
# import platform

from ..functions import display_template_information, erase_lines
from ..questions import GenerateQuestions, CommonQuestions
from ..wizard_text import Text
from ...constants import (YES, NO, LATEST, USE_LATEST, ALWAYS_ASK, GENERATE_ALL_METHODOLOGY_TEMPLATES, CONFIG_FILE,
                          READ_MORE, DOWNLOAD, GENERATE, EMAIL_APPROVER, MMC_GITHUB_SETUP, MMC_GITHUB_SETUP_LINK)
from ...core.registry.versioned_template import VersionedTemplate
# from ...core.email_approver import email_approver
from ...fsm import Transition, State

logger = logging.getLogger('gryphon')


def _condition_confirmation_to_install(context: dict) -> bool:
    confirmed = context["confirmation_response"]
    return confirmed == YES


def _callback_confirmation_to_install(context: dict) -> dict:
    erase_lines(n_lines=len(context["extra_parameters"]) + 3 + context["n_lines"])
    return context


class Confirmation(State):
    name = "confirmation"
    transitions = [
        Transition(
            next_state="install",
            condition=_condition_confirmation_to_install
        ),
    ]

    def __init__(self, registry):
        self.templates = registry.get_templates(GENERATE)
        #self.templates.update(registry.get_templates(DOWNLOAD))
        
        with open(CONFIG_FILE, "r+", encoding="utf-8") as f:
            self.settings = json.load(f)
        super().__init__()

    def on_start(self, context: dict) -> dict:

        if "templates" not in context:
            context["templates"] = self.templates

        context["confirmation_response"] = GenerateQuestions.confirm_generate_all()

        return context
