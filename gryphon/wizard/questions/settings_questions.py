import questionary
from questionary import Choice, Separator
from .common_functions import base_question, get_back_choice
from ..wizard_text import Text
from ...constants import (YES, NO, NAME, VALUE)


class SettingsQuestions:

    base_choices = [
        Choice(
            title="Yes",
            value=YES
        ),
        Choice(
            title="No, go back to the previous menu.",
            value=NO
        )
    ]

    @staticmethod
    @base_question
    def get_option(categories: list):
        categories = [
            Choice(
                title=c[NAME],
                value=c.get(VALUE, c[NAME])
            )
            for c in categories
        ]
        categories.extend([
            Separator(Text.menu_separator),
            get_back_choice()
        ])

        return questionary.select(
            message=Text.add_prompt_categories_question,
            choices=categories,
            instruction=Text.add_prompt_instruction
        ).unsafe_ask()

    @base_question
    def confirm_restore_defaults(self):
        return questionary.select(
            message=Text.settings_confirm_restore_defaults,
            choices=self.base_choices
        ).unsafe_ask()

    @base_question
    def confirm_restore_registry_defaults(self):
        return questionary.select(
            message=Text.settings_confirm_restorer_registry_defaults,
            choices=self.base_choices
        ).unsafe_ask()

    @base_question
    def confirm_registry_addition(self, registry_name):
        return questionary.select(
            message=Text.settings_confirm_registry_addition.replace("{registry_name}", registry_name),
            choices=self.base_choices
        ).unsafe_ask()

    @base_question
    def confirm_remove_registry(self):
        return questionary.select(
            message=Text.settings_confirm_remove_registry,
            choices=self.base_choices
        ).unsafe_ask()

    @base_question
    def confirm_change_env_manager(self, env_manager):
        return questionary.select(
            message=Text.settings_confirm_change_env_manager.replace("{env_manager}", env_manager),
            choices=self.base_choices
        ).unsafe_ask()

    @staticmethod
    @base_question
    def ask_which_registry_to_remove(registries):
        choices = [
            Choice(
                title=f"{name} ({type_})",
                value=name
            )
            for name, type_ in registries.items()
        ]
        choices.extend([
            Separator(),
            get_back_choice()
        ])
        return questionary.select(
            message=Text.settings_ask_which_registry_delete,
            choices=choices
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
            .path(message=Text.settings_ask_local_path)
            .unsafe_ask()
        )
