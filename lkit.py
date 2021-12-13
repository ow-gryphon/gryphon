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
BACK = "back"

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


def erase_lines(n_lines=2):
    for _ in range(n_lines):
        print("\033[A                             \033[A")


def add():
    """add templates based on arguments and configurations."""
    with open(DATA_PATH / "lib_category_tree.json") as file:
        lib_tree = json.load(file)

    level = -1
    # loop to return to the category prompt
    while True:
        level += 1
        possibilities = list(lib_tree.keys())
        possibilities.remove("leaf_libraries")

        choices = {
            option: "category"
            for option in possibilities
        }

        choices.update({
            option: "library"
            for option in lib_tree["leaf_libraries"]
        })

        # categories
        library_name = questions.get_lib_category(list(choices.keys()))

        # type the bare lib name
        if library_name == "type":
            library_name = questions.get_lib_via_keyboard()
            break
        elif library_name == BACK:
            # return to the main menu
            erase_lines(n_lines=2 + level)
            return BACK
        elif choices[library_name] == "category":
            lib_tree = lib_tree[library_name]
            continue
        else:
            break

    questions.confirm_add(library_name)

    labskit_commands.add(
        library_name=library_name
    )


def generate():
    """generates templates based on arguments and configurations."""

    templates = commands.get_templates("generate")
    template_name = questions.ask_which_template(templates, command="generate")

    if template_name == BACK:
        erase_lines()
        return BACK

    template = templates[template_name]

    extra_parameters = questions.ask_extra_arguments(
        template.arguments,
        command="generate"
    )

    questions.confirm_generate(
        template_name=template.display_name,
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

    if template_name == BACK:
        erase_lines()
        return BACK

    template = templates[template_name]
    extra_parameters = questions.ask_extra_arguments(
        arguments=template.arguments,
        command="init"
    )

    questions.confirm_init(
        template_name=template.display_name,
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
     ██████  ██████  ██    ██ ██████  ██   ██  ██████  ███    ██ 
    ██       ██   ██  ██  ██  ██   ██ ██   ██ ██    ██ ████   ██ 
    ██   ███ ██████    ████   ██████  ███████ ██    ██ ██ ██  ██ 
    ██    ██ ██   ██    ██    ██      ██   ██ ██    ██ ██  ██ ██ 
     ██████  ██   ██    ██    ██      ██   ██  ██████  ██   ████ 
    
    Welcome to OW Gryphon your data and analytics toolkit!
    (press Ctrl+C at any time to quit)
    
    """)

    while True:
        chosen_command = questions.main_question()

        function = {
            "init": init,
            "generate": generate,
            "add": add,
            "about": lambda: print("Help and contacts"),
            "quit": exit
        }[chosen_command]
        try:
            response = function()
            if response != "back":
                break

        except Exception as er:
            Logging.error(f'Runtime error. {er}')
            exit(1)


# this enables us to use the cli without having to install each time
# by using `python lkit.py`
if __name__ == '__main__':
    main()
