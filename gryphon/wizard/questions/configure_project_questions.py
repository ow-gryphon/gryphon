from typing import Dict

import questionary
from questionary import Choice

from .common_functions import base_text_prompt
from ..wizard_text import Text
from ...constants import (NB_EXTENSIONS, NB_STRIP_OUT, PRE_COMMIT_HOOKS)


class ConfigureProjectQuestions:

    @staticmethod
    @base_text_prompt
    def ask_addons(current_states: Dict[str, bool]):
        return questionary.checkbox(
            message=Text.init_prompt_addons,
            choices=[
#                Choice(
#                    title="Notebook extensions",
#                    value=NB_EXTENSIONS,
#                    checked=current_states[NB_EXTENSIONS]
#                ),
                Choice(
                    title="Notebook stripout",
                    value=NB_STRIP_OUT,
                    checked=current_states[NB_STRIP_OUT]
                ),
                Choice(
                    title="Pre-commit hooks",
                    value=PRE_COMMIT_HOOKS,
                    checked=current_states[PRE_COMMIT_HOOKS]
                )
            ]
        ).unsafe_ask()
