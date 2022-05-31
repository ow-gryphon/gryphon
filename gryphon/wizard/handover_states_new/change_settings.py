from ..questions.handover_questions import HandoverQuestions
from ...constants import BACK, NO, YES
from ...core.common_operations import list_files
from ...core.operations import SettingsManager, RCManager
from ...fsm import State, Transition
from ...logger import logger
from ...wizard.functions import erase_lines


class ChangeSettings(State):
    name = "change_settings"
    transitions = [
    ]

    def on_start(self, context: dict) -> dict:

        context.pop("response", None)

        context["response"] = HandoverQuestions.confirm_to_proceed()

        return context
