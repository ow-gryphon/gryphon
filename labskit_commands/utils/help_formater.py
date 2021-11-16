"""
Help text generation.
"""


def get_command_help(metadata):
    """
    Gets a complete help string about the command.
    """
    help_string = """
    \bEXTRA PARAMETERS
    """

    for name, command in metadata.items():
        help_string += get_template_help(name, command)

    return help_string


def get_template_help(template_name, metadata):
    """
    Gets help string about the needed parameters to the given template.
    """
    l_b = """
    
    """
    help_string = f"""\n
    TEMPLATE={template_name}
    """
    try:
        arguments = metadata['metadata']["arguments"]
    except KeyError:
        return help_string + "\n\tNo additional parameters."

    args = [
        f"""
        {arg["name"]} - {arg.get("help", "")}
            type: {arg["type"]}
            required: {arg["required"]}"""
        for arg in arguments
    ]

    help_string += l_b.join(args)

    return help_string
