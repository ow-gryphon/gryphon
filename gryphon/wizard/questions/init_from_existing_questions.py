from pathlib import Path

import questionary
from questionary import Choice, Separator

from .common_functions import base_question, get_back_choice, logger
from ..functions import wrap_text
from ..wizard_text import Text
from ...constants import (YES, NO, CONDA)


class InitFromExistingQuestions:

    @staticmethod
    @base_question
    def ask_existing_location(template=None):
    
        if template is not None:
        
            yellow_text = ''
            if template.description:
                yellow_text = f"\t{template.description}\n"
                
            text, n_lines = wrap_text(yellow_text)
            logger.warning(text)
        
        return Path(questionary.path(message=Text.init_from_existing_prompt_location_question).unsafe_ask())
    
    
    @staticmethod
    @base_question
    def ask_project_info(template_name):

        message = (
            Text.init_ask_project_info
        )

        n_lines = len(message.split('\n'))

        options = [
            Choice(
                title="Yes",
                value=YES
            ),
            Choice(
                title="No",
                value=NO
            )
        ]
        
        return questionary.select(
            message=message,
            choices=options
        ).unsafe_ask(), n_lines
    
    @staticmethod
    @base_question
    def confirm_use_existing_environment(env_manager):
        message = Text.init_from_existing_confirm_conda_question \
            if env_manager == CONDA else \
            Text.init_from_existing_confirm_venv_question

        return questionary.select(
            message=message,
            choices=[
                Choice(
                    title="Yes",
                    value=YES
                ),
                Choice(
                    title="No, ignore it",
                    value="no_ignore"
                ),
                Choice(
                    title="No, delete it",
                    value="no_delete"
                ),
                Separator(),
                get_back_choice()
            ]
        ).unsafe_ask()

    @staticmethod
    @base_question
    def ask_to_point_to_external_env():

        return (
            questionary.select(
                message=Text.init_from_existing_point_to_external_env,
                choices=[
                    Choice(
                        title="No, create a brand new one for me",
                        value=NO
                    ),
                    Choice(
                        title="Yes",
                        value=YES
                    ),
                    Separator(),
                    get_back_choice()
                ]
            )
            .unsafe_ask()
        )

    @staticmethod
    @base_question
    def ask_external_env_path():

        return Path(
            questionary.path(message=Text.init_from_existing_ask_external_env_path)
            .unsafe_ask()
        )
