import questionary
from questionary import Choice, Separator

from .common_functions import base_question, get_back_choice
from ..wizard_text import Text
from ...constants import (
    REPORT_BUG, FEEDBACK
)


class ContactUsQuestions:

    @staticmethod
    @base_question
    def feedback_or_bug():
        choices = [
            Choice(
                title=Text.feedback_display_option,
                value=FEEDBACK
            ),
            Choice(
                title=Text.report_bug_display_option,
                value=REPORT_BUG
            ),
            Separator(),
            get_back_choice()
        ]

        return questionary.select(
            message=Text.contact_us_type_question,
            choices=choices
        ).unsafe_ask()
