from ..functions import filter_chosen_option
from ...fsm import Transition, State
from ...constants import (
    USE_CASES, METHODOLOGY, TOPIC, SECTOR, CHILDREN
)


def filter_templates_by_category(state: dict) -> dict:
    
    found_templates = {}
    
    for name, template in state["templates"].items():
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
                        state["history"][2] in template.topic
                )
        ):
            found_templates[name] = template
            
    return found_templates


# CONDITIONS AND CALLBACKS
def _condition_has_children(context: dict) -> bool:
    return CHILDREN in context["node"]


def _condition_nothing_found(context: dict) -> bool:
    return (CHILDREN not in context["node"]) and not bool(len(context["filtered_templates"]))


def _condition_found(context: dict) -> bool:
    return (CHILDREN not in context["node"]) and bool(len(context["filtered_templates"]))


class FilterTemplates(State):
    name = "filter_templates"
    transitions = [
        Transition(
            next_state="nothing_found",
            condition=_condition_nothing_found,
        ),
        Transition(
            next_state="ask_template",
            condition=_condition_found,
        ),
        Transition(
            next_state="ask_category",
            condition=_condition_has_children
        )
    ]

    def on_start(self, context: dict) -> dict:
        context["node"] = filter_chosen_option(
            context["actual_selection"],
            context["template_tree"]
        )

        context["history"].append(context["actual_selection"])
        if CHILDREN not in context["node"]:
            context["filtered_templates"] = filter_templates_by_category(context)
        else:
            context["actual_selection"] = context["node"]

        return context
