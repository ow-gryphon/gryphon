from pathlib import Path
from .functions import erase_lines
from .questions import InitQuestions
from ..core import init as core_init
from ..constants import INIT, BACK, NO


def init(_, registry):
    """Creates a starter repository for analytics projects."""
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
            template_path=template.path,
            location=location,
            **extra_parameters
        )

        break
