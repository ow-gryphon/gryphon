import json
from typing import List, Dict, Tuple
from ..settings import list_conda_available_python_versions
from ..questions import InitQuestions
from ...finite_state_machine import State, Transition, negate_condition
from ...constants import BACK, INIT, ALWAYS_ASK, DEFAULT_PYTHON_VERSION, CONFIG_FILE


def _change_from_ask_parameters_to_main_menu(*_, **kwargs):
    chosen_version = kwargs["chosen_version"]
    return chosen_version == BACK


class AskParameters(State):
    def __init__(self, registry):
        self.templates = registry.get_templates(INIT)
        with open(CONFIG_FILE, "r+", encoding="utf-8") as f:
            self.settings = json.load(f)
        super().__init__(self.name, self.transitions)

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

    def on_start(self, *args, **kwargs) -> Tuple[List, Dict]:
        template_name = kwargs.get("template_name")
        template = self.templates[template_name]
        extra_parameters = InitQuestions.ask_extra_arguments(
            arguments=template.arguments
        )

        if self.settings.get("default_python_version") == ALWAYS_ASK:
            versions = list_conda_available_python_versions()
            chosen_version = InitQuestions.ask_python_version(versions)
        else:
            chosen_version = self.settings.get("default_python_version", DEFAULT_PYTHON_VERSION)

        kwargs.update(dict(
            extra_parameters=extra_parameters,
            chosen_version=chosen_version,
            template=template
        ))
        return list(args), dict(kwargs)
