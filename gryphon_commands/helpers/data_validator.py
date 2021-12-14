"""
Module containing utilities to validate the extra parameters given in CLI.
"""
from typing import Dict
from gryphon_commands.registry import Template
from gryphon_commands.logging import Logging
from .help_formater import get_template_help, get_command_help


def validate_parameters(parameters, template_name: str, existing_templates: Dict[str, Template]):

    try:
        assert template_name in existing_templates
    except AssertionError:
        message = f"Template \"{template_name}\" not found."
        Logging.log(get_command_help(existing_templates))
        raise RuntimeError(message)

    template = existing_templates[template_name]

    if not len(template.arguments):
        return {}

    num_required_parameters = sum(map(lambda x: x.get("required", False), template.arguments))
    num_given_parameters = len(parameters)

    if not num_given_parameters >= num_required_parameters:
        message = get_template_help(template_name, template)
        difference = num_required_parameters - num_given_parameters
        Logging.log(message)

        error = f"\n\nMissing {difference} required template arguments:\n"
        raise RuntimeError(error)

    # TODO: Validate also the case where num_given_parameters is
    #  strictly higher than num_required_parameters
    
    if num_given_parameters == num_required_parameters:
        return {
            field["name"]: parameters[index]
            for index, field in enumerate(template.arguments)
        }

    for field in template.arguments:
        if field.get("required", False):
            assert field["name"] in parameters
