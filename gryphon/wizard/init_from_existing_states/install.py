import json

from ..questions import CommonQuestions
from ...constants import CONDA, VENV
from ...constants import (
    INIT, ALWAYS_ASK, CONFIG_FILE,
    LATEST, USE_LATEST
)
from ...core.init_from_existing import init_from_existing
from ...core.registry.versioned_template import VersionedTemplate
from ...fsm import State


class Install(State):
    name = "install"
    transitions = []

    def __init__(self, registry):
        self.templates = registry.get_templates(INIT)

        with open(CONFIG_FILE, "r+", encoding="utf-8") as f:
            self.settings = json.load(f)
        super().__init__()

    def _get_template(self, template_name):
        selected_template = self.templates[template_name]

        if isinstance(selected_template, VersionedTemplate):
            if self.settings.get("template_version_policy") == USE_LATEST:
                template = selected_template[LATEST]

            elif self.settings.get("template_version_policy") == ALWAYS_ASK:
                chosen_version = CommonQuestions.ask_template_version(selected_template.available_versions)
                template = selected_template[chosen_version]
            else:
                raise RuntimeError(f'Value from "template_version_policy" not in the possible values [{USE_LATEST},'
                                   f' {ALWAYS_ASK}].\nGiven:{self.settings.get("template_version_policy")}')

        else:
            template = selected_template

        return template

    def on_start(self, context: dict) -> dict:

        env = VENV
        path = None
        external_path = None
        if context["found_conda"]:
            env = CONDA
            path = context["conda_path"]

        elif context["found_venv"]:
            env = VENV
            path = context["venv_path"]

        if "external_env_path" in context:
            external_path = context["external_env_path"]

        init_from_existing(
            template=self._get_template(context["template_name"]),
            location=context["location"],
            env_manager=env,
            existing_env_path=path,
            use_existing_environment=context["use_existing"],
            external_env_path=external_path,
            delete_existing=context["delete"]
        )

        return context
