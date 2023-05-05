import logging
import os
import platform
from pathlib import Path

from ..functions import erase_lines
from ..questions import InitFromExistingQuestions
from ...constants import YES, NO, EMAIL_RECIPIENT, EMAIL_RECIPIENT_CC
from ...fsm import State, Transition
from ...core.core_text import Text as CoreText

logger = logging.getLogger('gryphon')


def _change_from_ask_project_info_to_install(context: dict) -> bool:
    
    ask_project = context["ask_project"]
    
    if ask_project == YES:
        import webbrowser
        import urllib.parse

        subject = 'New Gryphon project'

        url_data = urllib.parse.urlencode(
            dict(
                to=EMAIL_RECIPIENT,
                cc=EMAIL_RECIPIENT_CC,
                subject=subject,
                body=CoreText.project_use_description_template
            )
        )

        webbrowser.open(f"mailto:?{url_data}".replace("+","%20"), new=0)
    
    return True


class AskProjectInfo(State):

    name = "ask_project_info"
    transitions = [
        Transition(
            next_state="install",
            condition=_change_from_ask_project_info_to_install
        )
    ]

    def on_start(self, context: dict) -> dict:
    
        template_name = context["template_name"]
        
        context["n_lines_warning"] = 0

        is_project, n_lines = InitFromExistingQuestions.ask_project_info(
            template_name=template_name
        )

        context.update(dict(
            n_lines=n_lines,
            ask_project=is_project
        ))
        return context
