"""
Module containing utilities to validate the extra parameters given in CLI.
"""
import logging
from typing import Dict
from .help_formater import get_template_help, get_command_help
from ...core.registry import Template


logger = logging.getLogger('gryphon')


def validate_parameters(parameters, template_name: str, existing_templates: Dict[str, Template]):

    try:
        assert template_name in existing_templates
    except AssertionError:
        message = f"Template \"{template_name}\" not found."
        logger.info(get_command_help(existing_templates))
        raise RuntimeError(message)

    template = existing_templates[template_name]

    if not len(template.arguments):
        return {}

    num_required_parameters = sum(map(lambda x: x.get("required", False), template.arguments))
    num_given_parameters = len(parameters)

    if num_given_parameters < num_required_parameters:
        message = get_template_help(template_name, template)
        difference = num_required_parameters - num_given_parameters
        logger.error(message)

        error = f"\n\nMissing {difference} required template arguments:\n"
        raise RuntimeError(error)

    if num_given_parameters > num_required_parameters:
        raise RuntimeError("Unexpected arguments were given.")

    if num_given_parameters == num_required_parameters:
        return {
            field["name"]: parameters[index]
            for index, field in enumerate(template.arguments)
        }

    for field in template.arguments:
        if field.get("required", False):
            assert field["name"] in parameters
