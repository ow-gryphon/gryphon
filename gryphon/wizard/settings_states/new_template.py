import logging

from ..functions import erase_lines
from ..questions import SettingsQuestions, InitQuestions
from ...constants import NO, YES, CHANGE_LOCATION
from ...core.template_scaffolding import template_scaffolding
from ...fsm import State, Transition

logger = logging.getLogger('gryphon')


def back_to_previous(history, **kwargs):
    history.pop()
    erase_lines(**kwargs)


#####
def _condition_from_new_template_to_end(context: dict) -> bool:
    return context["confirmation_option"] == YES


def _callback_from_new_template_to_end(context: dict) -> dict:
    template_scaffolding(context["location"])

    context["history"] = []
    print("\n")
    return context


#####
def _condition_from_new_template_to_new_template(context: dict) -> bool:
    return context["confirmation_option"] == CHANGE_LOCATION


def _callback_from_new_template_to_new_template(context: dict) -> dict:
    erase_lines(n_lines=2)
    return context


####
def _condition_from_new_template_to_ask_option(context: dict) -> bool:
    return context["confirmation_option"] == NO


def _callback_from_from_new_template_to_ask_option(context: dict) -> dict:
    # remove 2 entries from history
    back_to_previous(context["history"], n_lines=2)
    back_to_previous(context["history"], n_lines=1)
    return context


class NewTemplate(State):
    name = "new_template"
    transitions = [
        Transition(
            next_state="ask_option",
            condition=_condition_from_new_template_to_ask_option,
            callback=_callback_from_from_new_template_to_ask_option
        ),
        Transition(
            next_state="ask_option",
            condition=_condition_from_new_template_to_end,
            callback=_callback_from_new_template_to_end
        ),
        Transition(
            next_state="perform_action",
            condition=_condition_from_new_template_to_new_template,
            callback=_callback_from_new_template_to_new_template
        )
    ]

    def on_start(self, context: dict) -> dict:
        # ask for the folder
        context["location"] = InitQuestions.ask_just_location()
        context["confirmation_option"] = SettingsQuestions.confirm_new_template(context["location"])
        return context
