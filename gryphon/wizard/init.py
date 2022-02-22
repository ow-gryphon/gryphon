import json
from pathlib import Path
from .settings import list_conda_available_python_versions
from .functions import erase_lines
from .questions import InitQuestions
from ..core import init as core_init
from ..constants import (
    INIT, BACK, NO, CONFIG_FILE, DEFAULT_PYTHON_VERSION,
    ALWAYS_ASK
)


def init(_, registry):
    """Creates a starter repository for analytics projects."""

    with open(CONFIG_FILE, "r+", encoding="utf-8") as f:
        settings = json.load(f)

    templates = registry.get_templates(INIT)

    while True:
        template_name, location = InitQuestions.ask_which_template(templates)

        if template_name == BACK:
            erase_lines()
            return BACK

        template = templates[template_name]
        extra_parameters = InitQuestions.ask_extra_arguments(
            arguments=template.arguments
        )

        if settings.get("default_python_version") == ALWAYS_ASK:
            versions = list_conda_available_python_versions()
            possible_versions = list(filter(
                lambda x: x.split(".")[0] >= "3" and int(x.split(".")[1]) >= 6,
                versions
            ))
            chosen_version = InitQuestions.ask_python_version(possible_versions)
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
