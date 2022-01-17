import json
import logging
from typing import Dict
from gryphon.core.registry import Template
import gryphon.core as gryphon
from .functions import (
    display_template_information, erase_lines,
    get_current_tree_state, get_option_names_generate)
from .constants import (
    USE_CASES, METHODOLOGY, TOPIC, SECTOR, SEARCH_BY_KEYWORD,
    BACK, LEAF_OPTIONS, QUIT, GENERATE
)
from .wizard_text import Text
from .questions import Questions


logger = logging.getLogger('gryphon')


class ContinueSignal(Exception):
    def __init__(self):
        super().__init__()


class ReturnSignal(Exception):
    def __init__(self, *args):
        super().__init__(*args)


def decrease_level(level, amount=1):
    # print("decrease", level, amount)
    return level - amount


def filter_by_keyword(keyword_to_find, templates: Dict[str, Template]):
    if keyword_to_find not in ['', ' ']:
        return {
            name: template
            for name, template in templates.items()
            if keyword_to_find.lower() in '\t'.join(template.keywords).lower()
        }
    return []


def handle_back_option(state: dict):
    if state["actual_selection"] != SEARCH_BY_KEYWORD:
        if len(state["history"]):
            state["history"].pop()
        erase_lines(n_lines=2)
    else:
        erase_lines(n_lines=3)


def back_to_previous_menu(state: dict):
    state["level"] = decrease_level(state["level"])

    if state["level"] < 0:
        # return to the main menu
        erase_lines(n_lines=2)
        raise ReturnSignal(BACK)
    else:
        handle_back_option(state)
        raise ContinueSignal()


def filter_templates_by_category(state: dict):
    return {
        name: template
        for name, template in state["templates"].items()
        if (
            (state["history"][0] == METHODOLOGY and (state["history"][1] in template.methodology)) or
            (state["history"][0] == USE_CASES and (state["history"][1] == SECTOR)
                and (state["history"][2] in template.sector)) or
            (state["history"][0] == USE_CASES and (state["history"][1] == TOPIC)
                and (state["history"][3] in template.topic))
        )
    }


def ask_what_to_do_if_nothing_found(state: dict):
    response = Questions.nothing_found()
    if response == QUIT:
        raise ReturnSignal()

    if response == BACK:
        handle_back_option(state)
        state["level"] = decrease_level(state["level"])
        raise ContinueSignal()


def ask_which_template(state: dict):
    template_name = Questions.ask_which_template(state["templates"], command=GENERATE)

    if template_name == BACK:
        handle_back_option(state)
        state["level"] = decrease_level(state["level"])
        raise ContinueSignal()

    return template_name


def generate(data_path, registry):
    """generates templates based on arguments and configurations."""
    template_name = ""

    with open(data_path / "template_category_tree.json") as file:
        full_tree = json.load(file)

    state = dict(
        level=0,
        template_name="",
        history=[],
        actual_selection=None,
        templates=registry.get_templates(GENERATE)
    )

    while True:
        try:
            filtered_templates = []
            template_tree = get_current_tree_state(
                tree=full_tree,
                history=state["history"]
            )

            # create a list with the current possible options
            possibilities = get_option_names_generate(template_tree)

            # categories
            state["actual_selection"] = Questions.get_generate_option(possibilities)
            # state["level"] += 1

            if state["actual_selection"] == SEARCH_BY_KEYWORD:
                keyword = Questions.generate_keyword_question()
                filtered_templates = filter_by_keyword(keyword, state["templates"])

            elif state["actual_selection"] == BACK:
                back_to_previous_menu(state)

            elif state["actual_selection"] in template_tree[LEAF_OPTIONS]:
                # this is the leaf item
                # filter the templates for that tree level
                state["history"].append(state["actual_selection"])
                filtered_templates = filter_templates_by_category(state)
                state["level"] = decrease_level(state["level"], amount=-1)

            else:
                # we are not in the leaf yet
                state["history"].append(state["actual_selection"])
                state["level"] = decrease_level(state["level"], amount=-1)

                raise ContinueSignal()

            # No template was found with the given navigation/keyword
            if not len(filtered_templates):
                ask_what_to_do_if_nothing_found(state)

            template_name = ask_which_template(state)

        except ContinueSignal:
            # print("continue", state)
            continue
        except ReturnSignal as e:
            # print("return", state)
            return str(e)
        else:
            break

    template = state["templates"][template_name]

    display_template_information(template)

    if len(template.arguments):
        logger.debug(Text.generate_ask_extra_parameters)
        extra_parameters = Questions.ask_extra_arguments(template.arguments)

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
