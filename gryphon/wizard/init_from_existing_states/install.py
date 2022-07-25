import json

from ..questions import CommonQuestions
from ...constants import CONDA, VENV
from ...constants import (
    INIT, ALWAYS_ASK, LATEST, USE_LATEST, YES
)
from ...core.init_from_existing import init_from_existing
from ...core.operations import SettingsManager
from ...core.registry.versioned_template import VersionedTemplate
from ...fsm import State


class Install(State):
    name = "install"
    transitions = []

    def __init__(self, registry):
        self.templates = registry.get_templates(INIT)

        with open(SettingsManager.get_config_path(), "r+", encoding="utf-8") as f:
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

        path = None
        external_path = None
        if context["use_existing"]:

            if context["found_conda"]:
                env = CONDA
                path = context["conda_path"]

            elif context["found_venv"]:
                env = VENV
                path = context["venv_path"]

            else:
                raise RuntimeError("Flag 'use_existing' was set without setting 'found_venv' neither 'found_conda'")

        elif "external_env_path" in context and context["point_to_external_env"] == YES:

            external_path = context["external_env_path"]
            if (external_path / "conda-meta").is_dir():
                env = CONDA
            else:
                env = VENV

            if context["delete"]:
                if context["found_conda"]:
                    path = context["conda_path"]

                elif context["found_venv"]:
                    path = context["venv_path"]

        else:
            env = SettingsManager.get_environment_manager()

            if context["delete"]:
                if context["found_conda"]:
                    path = context["conda_path"]

                elif context["found_venv"]:
                    path = context["venv_path"]

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
