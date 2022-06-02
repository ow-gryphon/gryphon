from ..questions.handover_questions import HandoverQuestions
from ...constants import BACK, NO, YES
from ...core.common_operations import list_files
from ...core.operations import SettingsManager, RCManager
from ...fsm import State, Transition
from ...logger import logger
from ...wizard.functions import erase_lines


def _condition_back_to_settings(_):
    return True


def _callback_back_to_settings(context):
    erase_lines(n_lines=2)
    return context


def _condition_change_size_limits(context):
    return context["response"] == "change_size_limits"


class ChangeGryphonFilesPolicy(State):
    name = "change_gryphon_files_policy"
    transitions = [
        Transition(
            next_state="change_settings",
            condition=_condition_back_to_settings,
            callback=_callback_back_to_settings
        )
    ]

    def on_start(self, context: dict) -> dict:

        context.pop("response", None)

        context["response"] = HandoverQuestions.choose_gryphon_files_policy()

        keep_gryphon_files = context["response"] == YES

        logfile = RCManager.get_rc_file(folder=context["location"])
        RCManager.set_handover_include_gryphon_generated_files(keep_gryphon_files, logfile=logfile)

        return context
