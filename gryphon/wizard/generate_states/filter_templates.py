from ..functions import filter_chosen_option
from ...fsm import Transition, State, negate_condition
from ...constants import (
    USE_CASES, METHODOLOGY, TOPIC, SECTOR, CHILDREN
)


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


# CONDITIONS AND CALLBACKS
def _condition_filter_templates(context: dict) -> bool:
    return CHILDREN not in context["node"]


def _callback_leaf_item(context: dict) -> dict:
    # this is the leaf item
    # filter the templates for that tree level
    context["history"].append(context["actual_selection"])
    context["filtered_templates"] = filter_templates_by_category(context)
    return context


def _callback_node_item(context: dict) -> dict:
    # we are not in the leaf yet
    context["history"].append(context["actual_selection"])
    context["actual_selection"] = context["node"]
    return context


class FilterTemplates(State):
    name = "filter_templates"
    transitions = [
        Transition(
            next_state="nothing_found",
            condition=_condition_filter_templates,
            callback=_callback_leaf_item
        ),
        Transition(
            next_state="ask_category",
            condition=negate_condition(_condition_filter_templates),
            callback=_callback_node_item
        )
    ]

    def on_start(self, context: dict) -> dict:
        context["node"] = filter_chosen_option(
            context["actual_selection"],
            context["template_tree"]
        )
        return context
