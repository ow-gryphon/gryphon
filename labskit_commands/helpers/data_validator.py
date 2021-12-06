"""
Module containing utilities to validate the extra parameters given in CLI.
"""
from labskit_commands.logging import Logging
from .help_formater import get_template_help, get_command_help


def validate_parameters(parameters, template_type, metadata):

    try:
        assert template_type in metadata
    except AssertionError:
        message = f"Template \"{template_type}\" not found."
        Logging.log(get_command_help(metadata))
        raise RuntimeError(message)

    argument_metadata = metadata[template_type]['metadata']

    try:
        argument_metadata = argument_metadata['arguments']
    except KeyError:
        return {}

    num_required_parameters = sum(map(lambda x: x.get("required", False), argument_metadata))
    num_given_parameters = len(parameters)

    if not num_given_parameters >= num_required_parameters:
        message = get_template_help(template_type, metadata[template_type])
        difference = num_required_parameters - num_given_parameters
        Logging.log(message)

        error = f"\n\nMissing {difference} required template arguments:\n"
        raise RuntimeError(error)

    # TODO: Validate also the case where num_given_parameters is
    #  strictly higher than num_required_parameters
    
    if num_given_parameters == num_required_parameters:
        return {
            field["name"]: parameters[index]
            for index, field in enumerate(argument_metadata)
        }

    for field in metadata:
        if field.get("required", False):
            assert field["name"] in parameters
