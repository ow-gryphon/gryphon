import json
from ..questions import GenerateQuestions
from ..functions import (
    erase_lines, get_current_tree_state, get_option_names, BackSignal
)
from ...fsm import Transition, State
from ...constants import SEARCH_BY_KEYWORD, BACK, QUIT, GENERATE


def ask_what_to_do_if_nothing_found(state: dict):
    response = GenerateQuestions.nothing_found()
    if response == QUIT:
        exit(0)

    if response == BACK:
        erase_lines(n_lines=2)

    if len(state["history"]) >= 1:
        state["history"].pop()
    else:
        raise BackSignal()


def filter_by_keyword(keyword_to_find, templates):
    if keyword_to_find not in ['', ' ']:
        return {
            name: template
            for name, template in templates.items()
            if keyword_to_find.lower() in '\t'.join(template.keywords).lower()
        }
    return []


# CONDITIONS AND CALLBACKS
def _condition_ask_category_to_back(context: dict) -> bool:
    return context["actual_selection"] == BACK


def _callback_ask_category_to_back(context: dict) -> dict:
    erase_lines(n_lines=2)
    if len(context["history"]) >= 1:
        context["history"].pop()
    else:
        raise BackSignal()

    return context


def _condition_ask_category_to_ask_category(context: dict) -> bool:
    return context["actual_selection"] != SEARCH_BY_KEYWORD \
           and context["actual_selection"] != BACK


def _condition_ask_category_to_type_keyword(context: dict) -> bool:
    return context["actual_selection"] == SEARCH_BY_KEYWORD


def _callback_ask_category_to_type_keyword(context: dict) -> dict:
    keyword = GenerateQuestions.generate_keyword_question()
    context["filtered_templates"] = filter_by_keyword(keyword, context["templates"])
    return context


class AskCategory(State):
    name = "ask_category"
    transitions = [
        Transition(
            next_state="ask_category",
            condition=_condition_ask_category_to_back,
            callback=_callback_ask_category_to_back
        ),
        Transition(
            next_state="filter_templates",
            condition=_condition_ask_category_to_ask_category
        ),
        Transition(
            next_state="ask_category",
            condition=_condition_ask_category_to_type_keyword,
            callback=_callback_ask_category_to_type_keyword
        )
    ]

    def __init__(self, data_path, registry):
        with open(data_path / "category_tree.json", encoding="UTF-8") as file:
            self.full_tree = json.load(file)
        self.templates = registry.get_templates(GENERATE)
        super().__init__()

    def on_start(self, context: dict) -> dict:
        if "history" not in context:
            context["history"] = []

        if "templates" not in context:
            context["templates"] = self.templates

        if "filtered_templates" not in context:
            context["filtered_templates"] = {}

        context["template_tree"] = get_current_tree_state(
            tree=self.full_tree,
            history=context["history"]
        )

        # create a list with the current possible options
        possibilities = get_option_names(context["template_tree"])

        # categories
        context["actual_selection"] = GenerateQuestions.get_generate_option(possibilities)
        return context
