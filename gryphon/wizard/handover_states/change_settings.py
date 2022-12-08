from ..questions.handover_questions import HandoverQuestions
from ...constants import BACK, NO, YES
from ...core.common_operations import list_files
from ...core.operations import SettingsManager, RCManager
from ...fsm import State, Transition
from ...logger import logger
from ...wizard.functions import erase_lines


def _condition_back_to_settings(context):
    return context["response"] == BACK


def _callback_back_to_settings(context):
    erase_lines(n_lines=2)
    erase_lines(n_lines=context["extra_lines"])
    context["extra_lines"] = 0
    return context


def _condition_change_size_limits(context):
    return context["response"] == "change_size_limits"


def _condition_change_gryphon_files_policy(context):
    return context["response"] == "change_gryphon_files_policy"


def _condition_change_large_files_policy(context):
    return context["response"] == "change_large_files_policy"


class ChangeSettings(State):
    name = "change_settings"
    transitions = [
        Transition(
            next_state="confirm_settings",
            condition=_condition_back_to_settings,
            callback=_callback_back_to_settings
        ),
        Transition(
            next_state="change_size_limits",
            condition=_condition_change_size_limits
        ),
        Transition(
            next_state="change_gryphon_files_policy",
            condition=_condition_change_gryphon_files_policy
        ),
        Transition(
            next_state="change_large_files_policy",
            condition=_condition_change_large_files_policy
        )
    ]

    def on_start(self, context: dict) -> dict:

        context.pop("response", None)

        context["response"] = HandoverQuestions.choose_setting_to_change()

        return context
