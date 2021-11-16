"""
Module containing utilities to validate the extra parameters given in CLI.
"""
import click
from .help_formater import get_template_help, get_command_help


def validate_parameters(parameters, template_type, metadata):

    try:
        assert template_type in metadata
    except AssertionError:
        message = f"Error: Template \"{template_type}\" not found.\nAvaliable options:"
        click.secho(message, fg='red')
        click.echo(get_command_help(metadata))
        raise click.Abort()

    argument_metadata = metadata[template_type]['metadata']

    try:
        argument_metadata = argument_metadata['arguments']
    except KeyError:
        return {}

    num_required_parameters = sum(map(lambda x: x.get("required", False), argument_metadata))
    num_given_parameters = len(parameters)

    if not num_given_parameters >= num_required_parameters:
        message = get_template_help(template_type, metadata[template_type])
        difference =  num_required_parameters - num_given_parameters

        error = f"\n\nError: Missing {difference} required template arguments:\n"
        click.secho(error, fg='red')
        click.echo(message)
        raise click.Abort()

    #TODO: Validate also the case where num_given_parameters is
    # strictly higher than num_required_parameters
    
    if num_given_parameters == num_required_parameters:
        return {
            field["name"]: parameters[index]
            for index, field in enumerate(argument_metadata)
        }


    for field in metadata:
        if field.get("required", False):
            assert field["name"] in parameters
