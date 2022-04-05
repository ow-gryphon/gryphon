import json
from ...fsm import State, Transition
from ..functions import (
    erase_lines, get_current_tree_state_by_value,
    filter_chosen_option_by_value, BackSignal
)
from ..questions import SettingsQuestions
from ...constants import (
    BACK, CHILDREN, CONFIG_FILE, DEFAULT_ENV,
    NAME, VALUE
)


def handle_current_env_manager(tree_level):
    with open(CONFIG_FILE, "r", encoding="UTF-8") as f:
        current_env = json.load(f).get("environment_management", DEFAULT_ENV)

    response = []
    for p in tree_level:
        p = p.copy()
        name = p.pop(NAME)
        entry = dict(
            name=f"{name} (current)" if p[VALUE].lower() == current_env else name,
            **p
        )
        response.append(entry)
    return response


def _condition_from_ask_option_to_back(context: dict) -> bool:
    return context["actual_selection"] == BACK


def _callback_from_ask_option_to_next(context: dict) -> dict:
    context["history"].append(context["actual_selection"])
    context["option"] = filter_chosen_option_by_value(context["actual_selection"], context["current_tree"])
    return context


def _condition_from_ask_option_to_self(context: dict) -> bool:
    return context["actual_selection"] != BACK and CHILDREN in context["option"]


def _condition_from_ask_option_to_next(context: dict) -> bool:
    return context["actual_selection"] != BACK and CHILDREN not in context["option"]


def _callback_from_ask_option_to_back(context: dict) -> dict:
    erase_lines()

    if len(context["history"]):
        context["history"].pop()
    else:
        raise BackSignal()

    return context


class AskOption(State):
    name = "ask_option"
    transitions = [
        Transition(
            next_state="ask_option",
            condition=_condition_from_ask_option_to_back,
            callback=_callback_from_ask_option_to_back
        ),
        Transition(
            next_state="ask_option",
            condition=_condition_from_ask_option_to_self
        ),
        Transition(
            next_state="perform_action",
            condition=_condition_from_ask_option_to_next,
            callback=_callback_from_ask_option_to_next
        )
    ]

    def __init__(self, data_path):

        with open(data_path / "settings_tree.json", encoding="utf-8") as file:
            self.full_tree = json.load(file)

        super().__init__()

    def on_start(self, context: dict) -> dict:

        if "history" not in context:
            context["history"] = []

        context["current_tree"] = get_current_tree_state_by_value(
            tree=self.full_tree,
            history=context["history"]
        )

        if len(context["history"]) and context["history"][0] == "change_env_manager":
            context["current_tree"] = handle_current_env_manager(context["current_tree"])

        context["actual_selection"] = SettingsQuestions.get_option(context["current_tree"])

        context["option"] = []
        if context["actual_selection"] != BACK:
            context["history"].append(context["actual_selection"])
            context["option"] = filter_chosen_option_by_value(context["actual_selection"], context["current_tree"])

        return context
