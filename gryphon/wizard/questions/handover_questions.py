from pathlib import Path
import questionary

from .common_functions import base_question
from ..wizard_text import Text


class HandoverQuestions:

    @staticmethod
    @base_question
    def ask_project_folder():
        return Path(questionary.path(message=Text.handover_prompt_folder_question).unsafe_ask())
