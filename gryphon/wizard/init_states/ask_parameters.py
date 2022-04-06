import json
from ..functions import list_conda_available_python_versions
from ..questions import InitQuestions
from ...fsm import State, Transition, negate_condition
from ...core.registry import Template
from ...constants import (
    BACK, INIT, ALWAYS_ASK, DEFAULT_PYTHON_VERSION, CONFIG_FILE,
    LATEST, USE_LATEST
)


def _change_from_ask_parameters_to_main_menu(context):
    chosen_version = context["chosen_version"]
    return chosen_version == BACK


class AskParameters(State):

    def __init__(self, registry):
        self.templates = registry.get_templates(INIT)
        with open(CONFIG_FILE, "r+", encoding="utf-8") as f:
            self.settings = json.load(f)
        super().__init__()

    name = "ask_parameters"
    transitions = [
        Transition(
            next_state="main_menu",
            condition=_change_from_ask_parameters_to_main_menu
        ),
        Transition(
            next_state="confirmation",
            condition=negate_condition(_change_from_ask_parameters_to_main_menu),
        )
    ]

    # TODO: change the ci/cd to create a json file in the format:
    """
        [
            {"version": "v0.0.1"}, 
            {"version": "v0.0.2"}
        ]
        
        instead of
        
        {
            "v0.0.1": {},
            "v0.0.2": {}
        }
    """
    def on_start(self, context: dict) -> dict:

        template = self.templates[context["template_name"]]
        if self.settings.get("template_version_policy") == USE_LATEST:
            context["template"] = template[LATEST]

        elif self.settings.get("template_version_policy") == ALWAYS_ASK:
            chosen_version = InitQuestions.ask_template_version(template.available_versions)
            context["template"] = template[chosen_version]
        else:
            context["template"] = template

        context["location"] = InitQuestions.ask_init_location()

        context["extra_parameters"] = InitQuestions.ask_extra_arguments(
            arguments=context["template"].arguments
        )

        if self.settings.get("default_python_version") == ALWAYS_ASK:
            versions = list_conda_available_python_versions()
            context["chosen_version"] = InitQuestions.ask_python_version(versions)
        else:
            context["chosen_version"] = self.settings.get("default_python_version", DEFAULT_PYTHON_VERSION)

        context.update(dict(
            template=context["template"]
        ))
        return context
