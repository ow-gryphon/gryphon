import json
from ..questions import GenerateQuestions
from ..functions import (
    erase_lines, get_current_tree_state, get_option_names, BackSignal
)
from ...fsm import Transition, State
from ...constants import SEARCH_BY_KEYWORD, BACK, GENERATE, DOWNLOAD


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
            next_state="ask_keyword",
            condition=_condition_ask_category_to_type_keyword
        )
    ]

    def __init__(self, data_path, registry):
        with open(data_path / "category_tree.json", encoding="UTF-8") as file:
            self.full_tree = json.load(file)
        self.templates = registry.get_templates(GENERATE)
        
        # Add DOWNLOAD templates (which will be filtered at later stage)
        self.templates.update(registry.get_templates(DOWNLOAD))
        
        
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
        selected_category = GenerateQuestions.get_generate_option(possibilities, context=context)
        context["actual_selection"] = selected_category.split(" | ")[0]
        return context
