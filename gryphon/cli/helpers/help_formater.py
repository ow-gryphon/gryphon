"""
Help text generation.
"""
from typing import Dict
from gryphon.core.registry import Template


def get_command_help(templates: Dict[str, Template]):
    """
    Gets a complete help string about the command.
    """
    help_string = """
    \bEXTRA PARAMETERS
    """

    for name, template in templates.items():
        help_string += get_template_help(name, template)

    return help_string.replace('\n', '\n\n')


def get_template_help(template_name: str, template: Template):
    """
    Gets help string about the needed parameters to the given template.
    """
    l_b = """
    
    """
    help_string = f"""\n
    TEMPLATE={template_name}
    """
    if not len(template.arguments):
        return help_string + "\n\tNo additional parameters."

    args = [
        f"""
        {arg["name"]} - {arg.get("help", "")}
            type: {arg["type"]}
            required: {arg["required"]}"""
        for arg in template.arguments
    ]

    help_string += l_b.join(args)

    return help_string
