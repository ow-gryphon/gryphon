from ..functions import erase_lines
from ..questions import InitFromExistingQuestions
from ...constants import YES, NO, BACK
from ...fsm import State, Transition


def _back_callback_1(context):
    erase_lines(n_lines=2)
    erase_lines(n_lines=1)
    return context


def _back_callback_2(context):
    erase_lines(n_lines=2)
    erase_lines(n_lines=1)
    return context


def _change_from_ask_template_to_main_menu(context):
    return context["point_to_external_env"] == BACK and not(context["found_conda"] or context["found_venv"])


def _change_from_ask_use_existing(context):
    return context["point_to_external_env"] == BACK and (context["found_conda"] or context["found_venv"])


def _condition_ask_point_external(context):
    return context["point_to_external_env"] == YES


def _condition_install(context):
    return context["point_to_external_env"] == NO


class AskPointExternal(State):

    name = "ask_point_external"
    transitions = [
        Transition(
            next_state="ask_template",
            condition=_change_from_ask_template_to_main_menu,
            callback=_back_callback_1
        ),
        Transition(
            next_state="ask_use_existing",
            condition=_change_from_ask_use_existing,
            callback=_back_callback_2
        ),
        Transition(
            next_state="ask_external_env_path",
            condition=_condition_ask_point_external
        ),
        Transition(
            next_state="install",
            condition=_condition_install
        )
    ]

    def on_start(self, context: dict) -> dict:
        context["point_to_external_env"] = InitFromExistingQuestions.ask_to_point_to_external_env()

        return context
