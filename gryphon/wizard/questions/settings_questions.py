import json

import questionary
from questionary import Choice, Separator
from .common_functions import base_question, get_back_choice
from ..wizard_text import Text
from ...constants import (
    YES, NO, NAME, VALUE, ALWAYS_ASK, SYSTEM_DEFAULT, CHANGE_LOCATION,
    DATA_PATH, USE_LATEST
)


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

    @classmethod
    @base_question
    def confirm_restore_defaults(cls):
        return questionary.select(
            message=Text.settings_confirm_restore_defaults,
            choices=cls.base_choices
        ).unsafe_ask()

    @classmethod
    @base_question
    def confirm_restore_registry_defaults(cls):
        return questionary.select(
            message=Text.settings_confirm_restorer_registry_defaults,
            choices=cls.base_choices
        ).unsafe_ask()

    @classmethod
    @base_question
    def confirm_registry_addition(cls, registry_name):
        return questionary.select(
            message=Text.settings_confirm_registry_addition.replace("{registry_name}", registry_name),
            choices=cls.base_choices
        ).unsafe_ask()

    @classmethod
    @base_question
    def confirm_remove_registry(cls):
        return questionary.select(
            message=Text.settings_confirm_remove_registry,
            choices=cls.base_choices
        ).unsafe_ask()

    @classmethod
    @base_question
    def confirm_change_env_manager(cls, env_manager):
        return questionary.select(
            message=Text.settings_confirm_change_env_manager.replace("{env_manager}", env_manager),
            choices=cls.base_choices
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

    @staticmethod
    @base_question
    def ask_python_version(versions, current_version):
        with open(DATA_PATH / "python_versions_observations.json", "r", encoding="utf-8") as f:
            obs = json.load(f)

        message = Text.settings_python_use_system_default
        choices = [
            Choice(
                title=message if SYSTEM_DEFAULT != current_version else f"{message} (current)",
                value=SYSTEM_DEFAULT
            )
        ]

        choices.extend([
            Choice(
                title=(v if v != current_version else f"{v} (current)") +
                      (f' ({obs[v]})' if v in obs else ''),
                value=v
            )
            for v in versions
        ])

        choices.extend([
            Separator(),
            Choice(
                title=f"Always ask when creating a new project. "
                      f"{'(current)' if current_version == ALWAYS_ASK else ''}",
                value=ALWAYS_ASK
            ),
            get_back_choice()
        ])

        return questionary.select(
            message=Text.settings_ask_python_version,
            choices=choices,
            use_indicator=True
        ).unsafe_ask()

    @staticmethod
    @base_question
    def confirm_new_template(location):
        message = (
            Text.settings_confirm_new_template
            .replace("{location}", str(location))
        )

        return questionary.select(
            message=message,
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
                    title="Change project location",
                    value=CHANGE_LOCATION
                )
            ]
        ).unsafe_ask()

    @staticmethod
    @base_question
    def ask_template_version_policy(current_policy):

        return questionary.select(
            message="Chose the template version policy you want to use:",
            choices=[
                Choice(
                    title="Always ask" + (" (current)" if current_policy == ALWAYS_ASK else ""),
                    value=ALWAYS_ASK
                ),
                Choice(
                    title="Use latest version" + (" (current)" if current_policy == USE_LATEST else ""),
                    value=USE_LATEST
                ),
                Separator(),
                get_back_choice()
            ]
        ).unsafe_ask()
