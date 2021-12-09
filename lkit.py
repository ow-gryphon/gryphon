"""
LKit .
"""
import json
from pathlib import Path
import labskit_commands
from labskit_commands import questions
from labskit_commands.registry import RegistryCollection
from labskit_commands.logging import Logging

PACKAGE_PATH = Path(__file__).parent
DATA_PATH = PACKAGE_PATH / "labskit_commands" / "data"

# Load contents of configuration file
with open(DATA_PATH / "labskit_config.json", "r") as f:
    settings = json.load(f)

try:
    # loads registry of templates to memory
    commands = RegistryCollection.from_config_file(
        settings=settings,
        data_path=DATA_PATH / "template_registry"
    )
except Exception as e:
    Logging.error(f'Registry loading error. {e}')
    exit(1)


def add():
    """add templates based on arguments and configurations."""
    with open(DATA_PATH / "lib_category_tree.json") as file:
        lib_tree = json.load(file)

    categories = list(lib_tree.keys())

    chosen_category = questions.get_lib_category(categories)
    if chosen_category == "type":
        library_name = questions.get_lib_via_keyboard()
    else:
        library_name = questions.get_lib(lib_tree[chosen_category])

        if library_name == "type":
            library_name = questions.get_lib_via_keyboard()

    questions.confirm_add(library_name)

    labskit_commands.add(
        library_name=library_name
    )


def generate():
    """generates templates based on arguments and configurations."""

    templates = commands.get_templates("generate")
    template_name = questions.ask_which_template(templates, command="generate")

    template = templates[template_name]

    extra_parameters = questions.ask_extra_arguments(
        template.arguments,
        command="generate"
    )

    questions.confirm_generate(
        template_name=template_name,
        **extra_parameters
    )

    labskit_commands.generate(
        template_path=template.path,
        requirements=template.dependencies,
        **extra_parameters,
    )


def init():
    """Creates a starter repository for analytics projects."""
    templates = commands.get_templates("init")
    template_name, location = questions.ask_which_template(templates)

    template = templates[template_name]
    extra_parameters = questions.ask_extra_arguments(
        arguments=template.arguments,
        command="init"
    )

    questions.confirm_init(
        template_name=template.name,
        location=location,
        **extra_parameters
    )

    labskit_commands.init(
        template_path=template.path,
        location=location,
        **extra_parameters
    )


def main():
    print("""
     ██████  ██████  ██    ██ ███████ ███████ ██ ███    ██ 
    ██       ██   ██  ██  ██  ██      ██      ██ ████   ██ 
    ██   ███ ██████    ████   █████   █████   ██ ██ ██  ██ 
    ██    ██ ██   ██    ██    ██      ██      ██ ██  ██ ██ 
     ██████  ██   ██    ██    ██      ██      ██ ██   ████ 
    
    Welcome to Griffin your data and analytics toolkit!
    (press ctrl+C at any time to quit)
    """)
    chosen_command = questions.main_question()

    function = {
        "init": init,
        "generate": generate,
        "add": add
    }[chosen_command]
    try:
        function()
    except Exception as er:
        Logging.error(f'Runtime error. {er}')
        exit(1)


# this enables us to use the cli without having to install each time
# by using `python lkit.py`
if __name__ == '__main__':
    main()
