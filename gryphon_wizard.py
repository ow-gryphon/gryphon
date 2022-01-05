"""
LKit .
"""
import os
import json
import platform
from pathlib import Path
import gryphon
from gryphon import questions
from gryphon.registry import RegistryCollection
from gryphon.logging import Logging
from gryphon.text import Text

if platform.system() == "Windows":
    from colorama import init
    init()

PACKAGE_PATH = Path(__file__).parent
DATA_PATH = PACKAGE_PATH / "gryphon" / "data"
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
    with open(DATA_PATH / "library_category_tree.json") as file:
        lib_tree = json.load(file)

    level = -1
    # loop to return to the category prompt
    while True:
        level += 1
        possibilities = list(lib_tree.keys())
        possibilities.remove("leaf_options")

        choices = {
            option: "node"
            for option in possibilities
        }

        choices.update({
            option: "leaf"
            for option in lib_tree["leaf_options"]
        })

        # categories
        library_name = questions.get_add_option(list(choices.keys()))

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

    gryphon.add(
        library_name=library_name
    )


def generate():
    """generates templates based on arguments and configurations."""

    def filter_by_keyword(keyword_to_find):
        if keyword_to_find not in ['', ' ']:
            return {
                name: template
                for name, template in templates.items()
                if keyword_to_find.lower() in '\t'.join(template.keywords).lower()
            }
        return []

    def display_template_information(template):
        Logging.log(f"\n{template.description}\n")
        Logging.log(f"\tTopics: {', '.join(template.topic)}")
        Logging.log(f"\tSectors: {', '.join(template.sector)}")
        Logging.log(f"\tMethodology: {', '.join(template.methodology)}\n")

    with open(DATA_PATH / "template_category_tree.json") as file:
        template_tree = json.load(file)

    choices = list(template_tree.keys())
    templates = commands.get_templates("generate")

    # categories
    category = questions.get_generate_option(choices)

    navigation = category
    lines = 2
    if category != "Search by keyword":

        if category == BACK:
            # return to the main menu
            erase_lines(n_lines=lines)
            return BACK

        elif category == "Use-cases":
            lines += 1
            template_tree = template_tree[category]

            choices = list(template_tree.keys())
            choices.remove("leaf_options")

            navigation = questions.get_generate_option(choices)

            if navigation == BACK:
                # return to the main menu
                erase_lines(n_lines=lines)
                return BACK

        # subcategories
        lines += 1
        choices = template_tree[navigation]["leaf_options"]
        subcategory = questions.get_generate_option(choices)

        if subcategory == BACK:
            # return to the main menu
            erase_lines(n_lines=lines)
            return BACK

        # filter the templates for that tree level
        filtered_templates = {
            name: template
            for name, template in templates.items()
            if (
                (category == "Methodology" and (subcategory in template.methodology)) or
                (category == "Use-cases" and (subcategory in template.sector)) or
                (category == "Use-cases" and (subcategory in template.topic))
            )
        }
    else:
        keyword = "lala"
        # TODO: Pedir pra digitar a keyword
        filtered_templates = filter_by_keyword(keyword)

    if not len(filtered_templates):
        # TODO: Avisar que nao achou nada
        # TODO: Dar a opção de retornar
        pass

    lines += 1
    template_name = questions.ask_which_template(filtered_templates, command="generate")

    if template_name == BACK:
        # return to the main menu
        erase_lines(n_lines=lines)
        return BACK

    template = templates[template_name]

    display_template_information(template)

    Logging.log(Text.generate_ask_extra_parameters)

    extra_parameters = questions.ask_extra_arguments(
        template.arguments,
        command="generate"
    )

    questions.confirm_generate(
        template_name=template.display_name,
        **extra_parameters
    )

    gryphon.generate(
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
            template_description=template.description,
            location=Path(location).resolve(),
            **extra_parameters
        )

        if response == "no":
            exit()

        if response == "yes":
            break

        erase_lines(n_lines=5)
        location = questions.ask_init_location()

    gryphon.init(
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
            erase_lines(n_lines=1)
        else:
            os.system(f"""nohup xdg-open "{response}" """)
            os.system(f"""rm nohup.out""")
            erase_lines()


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
            # Logging.error(f'Runtime error. {er}')
            raise er


def did_you_mean_gryphon():
    Logging.log("Did you mean \"gryphon\"?")


# this enables us to use the cli without having to install each time
# by using `python gryphon_wizard.py`
if __name__ == '__main__':
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

    main()
