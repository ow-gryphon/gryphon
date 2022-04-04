import json
from pathlib import Path
from transitions import Machine, State
from wizard.settings import list_conda_available_python_versions
from wizard.functions import erase_lines
from wizard.questions import InitQuestions
from core import init as core_init
from constants import (
    INIT, BACK, NO, CONFIG_FILE, DEFAULT_PYTHON_VERSION,
    ALWAYS_ASK
)


class InitHandler:

    def __init__(self, registry):
        with open(CONFIG_FILE, "r+", encoding="utf-8") as f:
            self.settings = json.load(f)

        self.templates = registry.get_templates(INIT)
        self.template_name = ""
        self.location = ""

    @staticmethod
    def back_to_main_menu_action():
        erase_lines()
        return BACK

    def ask_template_action(self):
        self.template_name, self.location = InitQuestions.ask_which_template(self.templates)


def init(_, registry):
    """Creates a starter repository for analytics projects."""

    handler = InitHandler(registry)

    machine = Machine(
        handler,
        states=[
            State(
                name="ask_template",
                on_enter="ask_template_action"
            ),
            State(
                name="back_to_main_menu",
                on_enter="back_to_main_menu_action"
            )
        ]
    )

    machine.add_transition(
        source="",
        dest="",
        conditions=[]
    )

    with open(CONFIG_FILE, "r+", encoding="utf-8") as f:
        settings = json.load(f)

    templates = registry.get_templates(INIT)

    while True:
        template_name, location = InitQuestions.ask_which_template(templates)

        if template_name == BACK:
            erase_lines()
            return BACK

        if settings.get("default_python_version") == ALWAYS_ASK:
            versions = list_conda_available_python_versions()
            chosen_version = InitQuestions.ask_python_version(versions)
        else:
            chosen_version = settings.get("default_python_version", DEFAULT_PYTHON_VERSION)

        if chosen_version == BACK:
            erase_lines(n_lines=2 + len(extra_parameters) + 1)
            continue

        response, n_lines = InitQuestions.confirm_init(
            template=template,
            location=Path(location).resolve(),
            **extra_parameters
        )

        if response == NO:
            erase_lines(n_lines=n_lines + 2)
            continue

        if response == "change_location":
            erase_lines(n_lines=n_lines + 1)
            location = InitQuestions.ask_init_location()

        core_init(
            template=template,
            location=location,
            python_version=chosen_version,
            **extra_parameters
        )

        break
