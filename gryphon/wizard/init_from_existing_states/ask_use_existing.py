from ..functions import erase_lines
from ..questions import InitFromExistingQuestions
from ...constants import YES, BACK, CONDA, VENV
from ...fsm import State, Transition


def _back_callback(context):
    erase_lines(n_lines=4)
    return context


def _change_from_ask_template_to_main_menu(context):
    return context["use_existing"] == BACK


def _condition_ask_point_external_delete(context):
    return context["use_existing"] == "no_delete"


def _condition_ask_point_external_ignore(context):
    return context["use_existing"] == "no_ignore"


def _condition_ask_project_info(context):
    return context["use_existing"] == YES


def _install_using_existing(context):
    context["delete"] = False
    context["use_existing"] = True
    return context


def _install_deleting(context):
    context["delete"] = True
    context["use_existing"] = False
    return context


def _install_ignoring(context):
    context["delete"] = False
    context["use_existing"] = False
    return context


class AskUseExisting(State):

    name = "ask_use_existing"
    transitions = [
        Transition(
            next_state="ask_template",
            condition=_change_from_ask_template_to_main_menu,
            callback=_back_callback
        ),
        Transition(
            next_state="ask_project_info",
            condition=_condition_ask_project_info,
            callback=_install_using_existing
        ),
        Transition(
            next_state="ask_point_external",
            condition=_condition_ask_point_external_delete,
            callback=_install_deleting
        ),
        Transition(
            next_state="ask_point_external",
            condition=_condition_ask_point_external_ignore,
            callback=_install_ignoring
        )
    ]

    def on_start(self, context: dict) -> dict:
        if context["found_conda"]:
            context["use_existing"] = InitFromExistingQuestions.confirm_use_existing_environment(CONDA)

        elif context["found_venv"]:
            context["use_existing"] = InitFromExistingQuestions.confirm_use_existing_environment(VENV)
        else:
            context["use_existing"] = False
        return context
