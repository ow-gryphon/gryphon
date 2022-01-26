import logging
import platform
from pathlib import Path
from typing import Tuple
from textwrap import fill
from gryphon.constants import CHILDREN, NAME, VENV


logger = logging.getLogger('gryphon')


def erase_lines(n_lines=2):
    for _ in range(n_lines):
        print("\033[A                             \033[A")


def wrap_text(text) -> Tuple[str, int]:
    wrapped = ""
    for i in text.split('\n'):
        line = fill(
            i, width=100, drop_whitespace=False,
            expand_tabs=True, replace_whitespace=False,
            break_on_hyphens=False, subsequent_indent='\t'
        )
        wrapped += '\n' + line

    n_lines = len(wrapped.split('\n'))

    return wrapped, n_lines


def display_template_information(template) -> int:
    information = ""

    information += f'\t{template.display_name}\n\n\t{template.description}\n\n'

    if len(template.topic):
        information += f"\tTopics: {', '.join(template.topic)}\n"

    if len(template.sector):
        information += f"\tSectors: {', '.join(template.sector)}\n"

    if len(template.methodology):
        information += f"\tMethodology: {', '.join(template.methodology)}\n"

    wrapped, n_lines = wrap_text(information)
    logger.info(wrapped)

    return n_lines


def get_current_tree_state(tree, history):
    if not len(history):
        return tree

    tree_level = tree.copy()

    for item in history:
        tree_level = filter_chosen_option(item, tree_level).get(CHILDREN, [])

    return tree_level


def filter_chosen_option(option, tree):
    try:
        return list(filter(lambda x: x[NAME] == option, tree))[0]
    except IndexError:
        raise RuntimeError("Error in the menu navigation.")


def get_option_names(tree):
    return list(map(lambda x: x[NAME], tree))


def current_folder_has_venv():
    cwd = Path.cwd()
    if platform.system() == "Windows":
        activate_path = cwd / VENV / "Scripts" / "activate.bat"
    else:
        activate_path = cwd / VENV / "bin" / "activate"

    return activate_path.is_file()
