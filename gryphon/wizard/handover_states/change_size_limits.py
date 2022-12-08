from ..questions import HandoverQuestions
from ...core.operations.settings import SettingsManager
from ...fsm import State, Transition, negate_condition
from ...wizard.functions import erase_lines


def _condition_check_files_to_check_large_files(_):
    return True


def _callback_check_files(context):
    erase_lines(n_lines=3)
    return context


class ChangeSizeLimits(State):
    name = "change_size_limits"
    transitions = [
        Transition(
            next_state="change_settings",
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
