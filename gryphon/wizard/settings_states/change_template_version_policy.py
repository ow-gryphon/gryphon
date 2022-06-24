import logging

from ..functions import erase_lines
from ..questions import SettingsQuestions
from ...constants import BACK, SUCCESS, ALWAYS_ASK
from ...core.operations import RCManager, SettingsManager
from ...fsm import State, Transition, negate_condition

logger = logging.getLogger('gryphon')


def back_to_previous(history, **kwargs):
    history.pop()
    erase_lines(**kwargs)


def _condition_from_change_python_version_to_ask_option(context: dict) -> bool:
    return context["selected_option"] == BACK


def _callback_from_change_python_version_to_ask_option(context: dict) -> dict:
    back_to_previous(context["history"], n_lines=1)
    back_to_previous(context["history"], n_lines=1)
    return context


def _callback_from_change_python_version_to_end(context: dict) -> dict:
    manager = SettingsManager()
    manager.change_template_version_policy(context["selected_option"])
    if context["selected_option"] == ALWAYS_ASK:
        logger.log(SUCCESS, f"The template versions will be asked every time.")
    else:
        logger.log(SUCCESS, f'Gryphon will use always the latest version of a template.')

    context["history"] = []
    print("\n")
    return context


class ChangeTemplateVersionPolicy(State):
    name = "change_template_version_policy"
    transitions = [
        Transition(
            next_state="ask_option",
            condition=_condition_from_change_python_version_to_ask_option,
            callback=_callback_from_change_python_version_to_ask_option
        ),
        Transition(
            next_state="ask_option",
            condition=negate_condition(_condition_from_change_python_version_to_ask_option),
            callback=_callback_from_change_python_version_to_end
        )
    ]

    def on_start(self, context: dict) -> dict:
        current_policy = RCManager.get_current_template_version_policy()
        context["selected_option"] = SettingsQuestions.ask_template_version_policy(current_policy)

        return context
