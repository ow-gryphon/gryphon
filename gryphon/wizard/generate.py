import json
import logging
import gryphon.core as gryphon
from .functions import (display_template_information, erase_lines, filter_by_keyword)
from .constants import *
from .wizard_text import Text
from .questions import Questions


logger = logging.getLogger('gryphon')


def generate(data_path, registry):
    """generates templates based on arguments and configurations."""

    while True:
        with open(data_path / "template_category_tree.json") as file:
            template_tree = json.load(file)

        choices = list(template_tree.keys())
        templates = registry.get_templates("generate")

        # categories
        category = Questions.get_generate_option(choices)

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

                navigation = Questions.get_generate_option(choices)

                if navigation == BACK:
                    # return to the main menu
                    erase_lines(n_lines=lines - 1)
                    continue

            # subcategories
            lines += 1
            choices = template_tree[navigation]["leaf_options"]
            subcategory = Questions.get_generate_option(choices)

            if subcategory == BACK:
                # return to the main menu
                erase_lines(n_lines=lines - 1)
                continue

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
            lines += 1
            keyword = Questions.generate_keyword_question()
            filtered_templates = filter_by_keyword(keyword, templates)

        if not len(filtered_templates):
            lines += 1
            response = Questions.nothing_found()
            if response == "quit":
                return

            if response == BACK:
                erase_lines(n_lines=lines - 1)
                continue

        lines += 1
        template_name = Questions.ask_which_template(filtered_templates, command="generate")

        if template_name == BACK:
            # return to the main menu
            erase_lines(n_lines=lines - 1)
            continue

        template = templates[template_name]

        display_template_information(template)

        if len(template.arguments):
            logger.debug(Text.generate_ask_extra_parameters)

            extra_parameters = Questions.ask_extra_arguments(
                template.arguments,
                command="generate"
            )
        else:
            extra_parameters = {}

        Questions.confirm_generate(
            template_name=template.display_name,
            **extra_parameters
        )

        gryphon.generate(
            template_path=template.path,
            requirements=template.dependencies,
            **extra_parameters,
        )
        break
