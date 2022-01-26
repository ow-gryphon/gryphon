import json
import logging
from typing import Dict
from gryphon.core.registry import Template
import gryphon.core as gryphon
from .functions import (
    display_template_information, erase_lines, current_folder_has_venv,
    get_current_tree_state, get_option_names, filter_chosen_option
)
from gryphon.constants import (
    USE_CASES, METHODOLOGY, TOPIC, SECTOR, SEARCH_BY_KEYWORD,
    BACK, QUIT, GENERATE, NO, CHILDREN
)
from .wizard_text import Text
from .questions import GenerateQuestions


logger = logging.getLogger('gryphon')


class ContinueSignal(Exception):
    def __init__(self):
        super().__init__()


class ReturnSignal(Exception):
    def __init__(self, *args):
        super().__init__(*args)


def filter_by_keyword(keyword_to_find, templates: Dict[str, Template]):
    if keyword_to_find not in ['', ' ']:
        return {
            name: template
            for name, template in templates.items()
            if keyword_to_find.lower() in '\t'.join(template.keywords).lower()
        }
    return []


def back_to_previous_menu(state: dict):
    if state["actual_selection"] == SEARCH_BY_KEYWORD:
        erase_lines(n_lines=3)
        raise ContinueSignal()
    else:
        erase_lines(n_lines=2)

    if len(state["history"]) >= 1:
        state["history"].pop()
        raise ContinueSignal()
    else:
        raise ReturnSignal(BACK)


def filter_templates_by_category(state: dict) -> dict:
    return {
        name: template
        for name, template in state["templates"].items()
        if (
            (
                state["history"][0] == METHODOLOGY and
                state["history"][1] in template.methodology
            ) or (
                state["history"][0] == USE_CASES and
                state["history"][1] == SECTOR and
                state["history"][2] in template.sector
            ) or (
                state["history"][0] == USE_CASES and
                state["history"][1] == TOPIC and
                state["history"][3] in template.topic
            )
        )
    }


def ask_what_to_do_if_nothing_found(state: dict):
    response = GenerateQuestions.nothing_found()
    if response == QUIT:
        exit(0)

    if response == BACK:
        back_to_previous_menu(state)


def ask_which_template(state: dict):
    template_name = GenerateQuestions.ask_which_template(state["filtered_templates"])
    if template_name == BACK:
        back_to_previous_menu(state)

    return template_name


def generate(data_path, registry):
    """generates templates based on arguments and configurations."""

    if not current_folder_has_venv():
        logger.warning(Text.no_virtual_environment_remainder)

    with open(data_path / "category_tree.json") as file:
        full_tree = json.load(file)

    state = dict(
        history=[],
        actual_selection=None,
        templates=registry.get_templates(GENERATE),
        filtered_templates={}
    )

    while True:
        try:
            template_tree = get_current_tree_state(
                tree=full_tree,
                history=state["history"]
            )

            # create a list with the current possible options
            possibilities = get_option_names(template_tree)

            # categories
            state["actual_selection"] = GenerateQuestions.get_generate_option(possibilities)

            if state["actual_selection"] == SEARCH_BY_KEYWORD:
                keyword = GenerateQuestions.generate_keyword_question()
                state["filtered_templates"] = filter_by_keyword(keyword, state["templates"])

            elif state["actual_selection"] == BACK:
                back_to_previous_menu(state)
            else:
                node = filter_chosen_option(state["actual_selection"], template_tree)
                if CHILDREN not in node:
                    # this is the leaf item
                    # filter the templates for that tree level
                    state["history"].append(state["actual_selection"])
                    state["filtered_templates"] = filter_templates_by_category(state)
                else:
                    # we are not in the leaf yet
                    state["history"].append(state["actual_selection"])
                    state["actual_selection"] = node
                    raise ContinueSignal()

            # No template was found with the given navigation/keyword
            if not len(state["filtered_templates"]):
                ask_what_to_do_if_nothing_found(state)

            while 1:
                template_name = ask_which_template(state)
                template = state["templates"][template_name]

                n_lines = display_template_information(template)

                extra_parameters = {}
                if len(template.arguments):
                    logger.info(Text.generate_ask_extra_parameters)
                    extra_parameters = GenerateQuestions.ask_extra_arguments(template.arguments)

                response = GenerateQuestions.confirm_generate(
                    template_name=template.display_name,
                    **extra_parameters
                )

                if response == NO:
                    erase_lines(n_lines=len(extra_parameters) + 2 + 1 + n_lines)
                    continue

                gryphon.generate(
                    template_path=template.path,
                    requirements=template.dependencies,
                    **extra_parameters,
                )

                break

        except ContinueSignal:
            continue
        except ReturnSignal as e:
            return str(e)
        else:
            break
