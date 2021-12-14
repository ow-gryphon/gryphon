"""
LKit .
"""
import json
import os
import platform
from pathlib import Path
import gryphon_commands
from gryphon_commands import questions
from gryphon_commands.registry import RegistryCollection
from gryphon_commands.logging import Logging
from gryphon_commands.text import Text

PACKAGE_PATH = Path(__file__).parent
DATA_PATH = PACKAGE_PATH / "gryphon_commands" / "data"
BACK = "back"

# Load contents of configuration file
with open(DATA_PATH / "gryphon_config.json", "r") as f:
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
        else:
            break

    questions.confirm_add(library_name)

    gryphon_commands.add(
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

    gryphon_commands.generate(
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

    while True:
        response = questions.confirm_init(
            template_name=template.display_name,
            location=Path(location).resolve(),
            **extra_parameters
        )

        if response == "no":
            exit()

        if response == "yes":
            break

        erase_lines(n_lines=5)
        location = questions.ask_init_location()

    gryphon_commands.init(
        template_path=template.path,
        location=location,
        **extra_parameters
    )


def about():
    Logging.log(Text.about)

    response = None
    while response != "quit":
        response = questions.prompt_about()

        if response == "quit":
            return

        if response == BACK:
            erase_lines(n_lines=8)
            return BACK

        if platform.system() == "Windows":
            os.system(f"start {response}")
        else:
            os.system(f"""nohup xdg-open "{response}" """)
            os.system(f"""rm nohup.out""")
        erase_lines()

        # TODO: get rid of winpty


def main():
    Logging.log(Text.welcome)

    while True:
        chosen_command = questions.main_question()

        function = {
            "init": init,
            "generate": generate,
            "add": add,
            "about": about,
            "quit": exit
        }[chosen_command]
        try:
            response = function()
            if response != BACK:
                break

        except Exception as er:
            Logging.error(f'Runtime error. {er}')
            exit(1)


def did_you_mean_gryphon():
    Logging.log("Did you mean \"gryphon\"?")


# this enables us to use the cli without having to install each time
# by using `python gryphon.py`
if __name__ == '__main__':
    main()
