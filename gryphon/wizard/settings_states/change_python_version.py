import logging

from ..functions import erase_lines, list_conda_available_python_versions
from ..questions import SettingsQuestions
from ...constants import BACK, SUCCESS, ALWAYS_ASK
from ...core.operations import SettingsManager
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
    manager.change_default_python_version(context["selected_option"])
    if context["selected_option"] == ALWAYS_ASK:
        logger.log(SUCCESS, f"The python version will be asked for every new project.")
    else:
        logger.log(SUCCESS, f'Default python version set to {context["selected_option"]}')

    context["history"] = []
    print("\n")
    return context


class ChangePythonVersion(State):
    name = "change_python_version"
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
        versions = list_conda_available_python_versions()
        context["selected_option"] = SettingsQuestions.ask_python_version(
            versions,
            SettingsManager.get_current_python_version()
        )

        return context
