import logging
from typing import Dict
from gryphon.core.registry import Template


logger = logging.getLogger('gryphon')


def erase_lines(n_lines=2):
    for _ in range(n_lines):
        print("\033[A                             \033[A")


def display_template_information(template):
    logger.info(f"\n{template.description}\n")
    logger.info(f"\tTopics: {', '.join(template.topic)}")
    logger.info(f"\tSectors: {', '.join(template.sector)}")
    logger.info(f"\tMethodology: {', '.join(template.methodology)}\n")


def filter_by_keyword(keyword_to_find, templates: Dict[str, Template]):
    if keyword_to_find not in ['', ' ']:
        return {
            name: template
            for name, template in templates.items()
            if keyword_to_find.lower() in '\t'.join(template.keywords).lower()
        }
    return []


def get_current_tree_state(tree, history):
    tree_level = tree.copy()

    for item in history:
        if item in tree_level:
            tree_level = tree_level[item]
        else:
            raise RuntimeError("Error in tree navigation.")

    return tree_level


