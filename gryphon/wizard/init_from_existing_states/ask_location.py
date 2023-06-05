from ...core.init_from_existing import check_for_environment
from ...fsm import State, Transition
from ...wizard.questions import InitFromExistingQuestions

import logging
import os
import json
logger = logging.getLogger('gryphon')

from ...constants import (
    BACK, INIT, ALWAYS_ASK, DEFAULT_PYTHON_VERSION, CONFIG_FILE,
    LATEST, USE_LATEST
)
from ...core.registry.versioned_template import VersionedTemplate


def _condition_ask_use_existing(context: dict) -> bool:
    return context["is_there_any_existing_environment"]


def _condition_ask_point_external(context: dict) -> bool:
    return not context["is_there_any_existing_environment"]


class AskLocation(State):

    def __init__(self, registry):
        self.templates = registry.get_templates(INIT)
        with open(CONFIG_FILE, "r+", encoding="utf-8") as f:
            self.settings = json.load(f)
        super().__init__()
        
    name = "ask_location"
    transitions = [
        Transition(
            next_state="ask_point_external",
            condition=_condition_ask_point_external
        ),
        Transition(
            next_state="ask_use_existing",
            condition=_condition_ask_use_existing
        )
    ]

    def on_start(self, context: dict) -> dict:
    
        template = self.templates[context["template_name"]]

        if isinstance(template, VersionedTemplate):
            if self.settings.get("template_version_policy") == USE_LATEST:
                template = template[LATEST]

            elif self.settings.get("template_version_policy") == ALWAYS_ASK:
                chosen_version = CommonQuestions.ask_template_version(template.available_versions)
                template = template[chosen_version]
                
        context["location"] = InitFromExistingQuestions.ask_existing_location(template)
        
        if not os.path.isdir(context["location"]):
            logger.warning(f"{context['location']} is not an existing folder. A new folder will be created if you proceed.")
        
        found_conda, found_venv, conda_path, venv_path = check_for_environment(context["location"])

        context["found_conda"], context["found_venv"] = found_conda, found_venv
        context["conda_path"], context["venv_path"] = conda_path, venv_path
        context["is_there_any_existing_environment"] = found_conda or found_venv
        context["use_existing"] = False
        return context
