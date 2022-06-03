from pathlib import Path
import questionary
from questionary import Choice, Separator

from .common_functions import base_question, get_back_choice
from ..wizard_text import Text
from ...constants import YES, NO, CHANGE_LIMIT


class NumberValidator(questionary.Validator):
    def validate(self, document):
        try:
            float(document.text)
        except ValueError:
            raise questionary.ValidationError(
                message="Not a valid number.",
                cursor_position=len(document.text)
            )


class HandoverQuestions:

    @staticmethod
    @base_question
    def ask_project_folder():
        return Path(questionary.path(message=Text.handover_prompt_folder_question).unsafe_ask())

    @staticmethod
    @base_question
    def ask_new_size_limit(limit):
        return float(questionary.text(
            message=Text.handover_prompt_new_size_limit_question.replace("{limit}", str(limit)),
            validate=NumberValidator
        ).unsafe_ask())

    @staticmethod
    @base_question
    def ask_large_files(limit):
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

    @staticmethod
    @base_question
    def confirm_to_proceed():
        return questionary.select(
            message=Text.handover_prompt_confirm_configurations,
            choices=[
                Choice(
                    title="Yes",
                    value=YES
                ),
                Choice(
                    title="No, change configurations",
                    value=NO
                ),
                Separator(),
                get_back_choice()
            ]
        ).unsafe_ask()

    @staticmethod
    @base_question
    def choose_setting_to_change():
        return questionary.select(
            message=Text.handover_prompt_change_settings,
            choices=[
                Choice(
                    title="Change file size limit",
                    value="change_size_limits"
                ),
                Choice(
                    title="Change whether to include Gryphon generated files",
                    value="change_gryphon_files_policy"
                ),
                Separator(),
                get_back_choice()
            ]
        ).unsafe_ask()

    @staticmethod
    @base_question
    def choose_gryphon_files_policy():
        return questionary.select(
            message=Text.handover_prompt_gryphon_files_policy,
            choices=[
                Choice(
                    title="DO include in the handover package",
                    value=YES
                ),
                Choice(
                    title="DO NOT include in the handover package",
                    value=NO
                )
            ]
        ).unsafe_ask()

    @staticmethod
    @base_question
    def choose_large_files_policy():
        return questionary.select(
            message=Text.handover_prompt_large_files_policy,
            choices=[
                Choice(
                    title="DO include in the handover package",
                    value=YES
                ),
                Choice(
                    title="DO NOT include in the handover package",
                    value=NO
                )
            ]
        ).unsafe_ask()
