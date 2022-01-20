import logging
from typing import Dict
from gryphon.core.registry import Template
from .constants import LEAF_OPTIONS, CHILDREN, NAME


logger = logging.getLogger('gryphon')


def erase_lines(n_lines=2):
    for _ in range(n_lines):
        print("\033[A                             \033[A")


def display_template_information(template) -> int:
    information = ""
    information += f"\n{template.description}\n"

    if len(template.topic):
        information += f"\tTopics: {', '.join(template.topic)}\n"

    if len(template.sector):
        information += f"\tSectors: {', '.join(template.sector)}\n"

    if len(template.methodology):
        information += f"\tMethodology: {', '.join(template.methodology)}\n"

    logger.info(information)
    return len(information.split("\n"))


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


def get_option_names_add(tree):
    return list(map(lambda x: x[NAME], tree))


def get_option_names_generate(tree):
    options = list(tree.keys())
    options.extend(list(tree[LEAF_OPTIONS]))
    options.remove(LEAF_OPTIONS)
    return options
