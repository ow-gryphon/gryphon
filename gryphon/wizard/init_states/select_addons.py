import logging

from ..functions import erase_lines
from ..questions import InitQuestions
from ...constants import BACK, PIPENV, NB_EXTENSIONS, NB_STRIP_OUT, PRE_COMMIT_HOOKS
from ...fsm import State, Transition
from ...fsm import negate_condition

logger = logging.getLogger('gryphon')


def _go_back_callback(context: dict) -> dict:
    erase_lines(n_lines=2)
    del context["selected_addons"]
    return context


def _go_back_from_divided_flow_callback(context: dict) -> dict:
    erase_lines(n_lines=context["n_lines_warning"])
    del context["n_lines_warning"]
    del context["selected_addons"]
    return context


def _go_back(context: dict) -> bool:
    return context["selected_addons"] == BACK and "n_lines_warning" not in context


def _go_back_from_divided_flow(context: dict) -> bool:
    return context["selected_addons"] == BACK and "n_lines_warning" in context


class SelectAddons(State):

    name = "select_addons"

    transitions = [
        Transition(
            next_state="ask_parameters",
            condition=_go_back,
            callback=_go_back_callback
        ),
        Transition(
            next_state="ask_location_again",
            condition=_go_back_from_divided_flow,
            callback=_go_back_from_divided_flow_callback
        ),
        Transition(
            next_state="confirmation",
            condition=lambda x: negate_condition(_go_back)(x) and negate_condition(_go_back_from_divided_flow)(x)
        )
    ]

    def on_start(self, context: dict) -> dict:
    
        template = context["template"]
        
        if template.addons:
            context["selected_addons"] = InitQuestions.ask_addons(template.addons)
        else:
            
            if template.force_env == PIPENV:
                context["selected_addons"] = InitQuestions.ask_addons([
                              {"addon_name": NB_EXTENSIONS, "checked": False}
                              ])
                
            else:
                context["selected_addons"] = InitQuestions.ask_addons()
            
            
        return context

# TODO: Implement the same logic in the project scaffold creation
# TODO: refactor tests to match the new user flow
