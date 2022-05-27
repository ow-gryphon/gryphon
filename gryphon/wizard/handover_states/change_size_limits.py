from ..questions import HandoverQuestions
from ...constants import BACK
from ...core.settings import SettingsManager
from ...fsm import State, Transition, negate_condition
from ...wizard.functions import erase_lines


def _condition_check_files_to_check_large_files(context):
    return context["new_limit"] < 0


def _callback_check_files(context):
    erase_lines(n_lines=2)
    erase_lines(n_lines=context["extra_lines"])
    return context


class ChangeSizeLimits(State):
    name = "change_size_limits"
    transitions = [
        Transition(
            next_state="check_large_files",
            condition=negate_condition(_condition_check_files_to_check_large_files),
        ),
        Transition(
            next_state="check_large_files",
            condition=_condition_check_files_to_check_large_files,
            callback=_callback_check_files
        )
    ]

    def on_start(self, context: dict) -> dict:
        limit = SettingsManager.get_handover_file_size_limit()
        context["new_limit"] = HandoverQuestions.ask_new_size_limit(limit)
        if context["new_limit"] >= 0:
            SettingsManager.change_handover_file_size_limit(context["new_limit"])

        return context
