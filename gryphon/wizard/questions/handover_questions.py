from pathlib import Path
import questionary
from questionary import Choice, Separator

from .common_functions import base_question, get_back_choice
from ..wizard_text import Text
from ...constants import YES, NO, CHANGE_LIMIT


class HandoverQuestions:

    @staticmethod
    @base_question
    def ask_project_folder():
        return Path(questionary.path(message=Text.handover_prompt_folder_question).unsafe_ask())

    @staticmethod
    @base_question
    def ask_large_files():
        limit = 10
        return questionary.select(
            message=Text.handover_prompt_include_large_files_question,
            choices=[
                Choice(
                    title="Yes",
                    value=YES
                ),
                Choice(
                    title="No",
                    value=NO
                ),
                Choice(
                    title=f"Change limit (current limit = {limit} MB)",
                    value=CHANGE_LIMIT
                ),
                Separator(),
                get_back_choice()
            ]
        ).unsafe_ask()
