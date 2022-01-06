from typing import Dict
from .logger import Logging
from gryphon.core.registry import Template


def erase_lines(n_lines=2):
    for _ in range(n_lines):
        print("\033[A                             \033[A")


def display_template_information(template):
    Logging.log(f"\n{template.description}\n")
    Logging.log(f"\tTopics: {', '.join(template.topic)}")
    Logging.log(f"\tSectors: {', '.join(template.sector)}")
    Logging.log(f"\tMethodology: {', '.join(template.methodology)}\n")


def filter_by_keyword(keyword_to_find, templates: Dict[str, Template]):
        if keyword_to_find not in ['', ' ']:
            return {
                name: template
                for name, template in templates.items()
                if keyword_to_find.lower() in '\t'.join(template.keywords).lower()
            }
        return []

