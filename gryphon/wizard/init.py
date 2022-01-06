from pathlib import Path
import gryphon.core as gryphon
from .constants import *
from .functions import *
from .questions import Questions


def init(_, registry):
    """Creates a starter repository for analytics projects."""
    templates = registry.get_templates("init")
    template_name, location = Questions.ask_which_template(templates)

    if template_name == BACK:
        erase_lines()
        return BACK

    template = templates[template_name]
    extra_parameters = Questions.ask_extra_arguments(
        arguments=template.arguments,
        command="init"
    )

    while True:
        response = Questions.confirm_init(
            template_name=template.display_name,
            template_description=template.description,
            location=Path(location).resolve(),
            **extra_parameters
        )

        if response == "no":
            exit()

        if response == "yes":
            break

        erase_lines(n_lines=5)
        location = Questions.ask_init_location()

    gryphon.init(
        template_path=template.path,
        location=location,
        **extra_parameters
    )
