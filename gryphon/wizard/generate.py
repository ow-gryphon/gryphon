import json
import logging
import gryphon.core as gryphon
from .functions import (
    display_template_information, erase_lines, filter_by_keyword,
    get_current_tree_state, get_option_names_generate)
from .constants import *
from .wizard_text import Text
from .questions import Questions


logger = logging.getLogger('gryphon')


def generate(data_path, registry):
    """generates templates based on arguments and configurations."""

    with open(data_path / "template_category_tree.json") as file:
        full_tree = json.load(file)

    level = 0
    template_name = ""
    navigation_history = []
    templates = registry.get_templates("generate")

    while True:

        template_tree = get_current_tree_state(
            tree=full_tree,
            history=navigation_history
        )

        # create a list with the current possible options
        possibilities = get_option_names_generate(template_tree)

        # categories
        chosen_option = Questions.get_generate_option(possibilities)

        if chosen_option == SEARCH_BY_KEYWORD:
            keyword = Questions.generate_keyword_question()
            filtered_templates = filter_by_keyword(keyword, templates)
            level += 1
        elif chosen_option == BACK:
            erase_lines(n_lines=2)

            if level == 0:
                # return to the main menu
                return BACK
            else:
                if len(navigation_history):
                    navigation_history.pop()
                level -= 1
                continue

        elif chosen_option in template_tree[LEAF_OPTIONS]:
            # this is the leaf item
            # filter the templates for that tree level
            filtered_templates = {
                name: template
                for name, template in templates.items()
                if (
                    (navigation_history[0] == METHODOLOGY and (chosen_option in template.methodology)) or
                    (navigation_history[0] == USE_CASES and (navigation_history[1] == "sector")
                     and (chosen_option in template.sector)) or
                    (navigation_history[0] == USE_CASES and (navigation_history[1] == "topic")
                     and (chosen_option in template.topic))
                )
            }
            navigation_history.append(chosen_option)
            level += 1
        else:
            # we are not in the leaf yet
            navigation_history.append(chosen_option)
            level += 1
            continue

        # No template was found with the given navigation/keyword
        if not len(filtered_templates):
            response = Questions.nothing_found()
            if response == QUIT:
                return

            if response == BACK:
                if not chosen_option == SEARCH_BY_KEYWORD:
                    navigation_history.pop()
                    erase_lines(n_lines=2)
                else:
                    erase_lines(n_lines=3)
                level -= 1
                continue

        template_name = Questions.ask_which_template(filtered_templates, command="generate")

        if template_name == BACK:
            # return to the main menu
            erase_lines(n_lines=2)
            level -= 1
            navigation_history.pop()
            continue
        else:
            break

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
