import questionary
from questionary import Choice
from .common_functions import base_question
from ..wizard_text import Text
from ...constants import (YES, NO)


class SettingsQuestions:

    @staticmethod
    @base_question
    def confirm_restore_defaults():
        return questionary.select(
            message=Text.settings_confirm_restore_defaults,
            choices=[
                Choice(
                    title="Yes",
                    value=YES
                ),
                Choice(
                    title="No, go back to the previous menu.",
                    value=NO
                )
            ]
        ).unsafe_ask()

    @staticmethod
    @base_question
    def confirm_restore_registry_defaults():
        return questionary.select(
            message=Text.settings_confirm_restore_defaults,
            choices=[
                Choice(
                    title="Yes",
                    value=YES
                ),
                Choice(
                    title="No, go back to the previous menu.",
                    value=NO
                )
            ]
        ).unsafe_ask()

    @staticmethod
    @base_question
    def ask_which_registry_to_remove(registries):
        return questionary.select(
            message=Text.settings_ask_which_registry_delete,
            choices=[
                Choice(
                    title=f"{name} ({type_})",
                    value=name
                )
                for name, type_ in registries.items()
            ]
        ).unsafe_ask()

    @staticmethod
    @base_question
    def ask_registry_name():
        return (
            questionary
            .text(message=Text.settings_ask_registry_name)
            .unsafe_ask()
        )

    @staticmethod
    @base_question
    def ask_git_url():
        return (
            questionary
            .text(message=Text.settings_ask_git_url)
            .unsafe_ask()
        )

    @staticmethod
    @base_question
    def ask_local_path():
        return (
            questionary
            .text(message=Text.settings_ask_local_path)
            .unsafe_ask()
        )
