import logging
import os
import platform
from pathlib import Path

from ..functions import erase_lines
from ..questions import DownloadQuestions
from ...constants import YES, NO, READ_MORE, CHANGE_LOCATION
from ...fsm import State, Transition

logger = logging.getLogger('gryphon')


def confirmation_success_callback(context: dict) -> dict:
    n_lines = context["n_lines"]
    ask_again = context["n_lines_ask_again"] if "n_lines_ask_again" in context else 0

    erase_lines(n_lines=n_lines + 2 + context["n_lines_warning"] + ask_again)
    return context


def ask_location_again_callback(context: dict) -> dict:
    n_lines = context["n_lines"]
    ask_again = context["n_lines_ask_again"] if "n_lines_ask_again" in context else 0

    erase_lines(n_lines=n_lines + 1 + context["n_lines_warning"] + ask_again)
    return context


def read_more_callback(context: dict) -> dict:
    n_lines = context["n_lines"]
    ask_again = context["n_lines_ask_again"] if "n_lines_ask_again" in context else 0

    if platform.system() == "Windows":
        os.system(f'start {context["read_more_link"]}')
    else:
        os.system(f"""nohup xdg-open "{context["read_more_link"]}" """)
        os.system(f"""rm nohup.out""")
        erase_lines(n_lines=1)

    erase_lines(n_lines=n_lines + context["n_lines_warning"] + ask_again)
    return context


def _change_from_confirmation_to_ask_project_info(context: dict) -> bool:
    confirmed = context["confirmed"]
    return confirmed == YES and not bool(context["template"].shell_exec)


def _change_from_confirmation_to_confirm_shell_exec(context: dict) -> bool:
    confirmed = context["confirmed"]
    return confirmed == YES and bool(context["template"].shell_exec)


def _change_from_confirmation_to_ask_template(context: dict) -> bool:
    confirmed = context["confirmed"]
    return confirmed == NO


def _change_from_confirmation_to_confirm(context: dict) -> bool:
    confirmed = context["confirmed"]
    return confirmed == READ_MORE


def _change_from_confirmation_to_ask_location_again(context: dict) -> bool:
    confirmed = context["confirmed"]
    return confirmed == CHANGE_LOCATION
    

class Confirmation(State):

    name = "confirmation"
    transitions = [
        Transition(
            next_state="ask_project_info",
            condition=_change_from_confirmation_to_ask_project_info
        ),
        Transition(
            next_state="ask_location_again",
            condition=_change_from_confirmation_to_ask_location_again,
            callback=ask_location_again_callback
        ),
        Transition(
            next_state="confirmation",
            condition=_change_from_confirmation_to_confirm,
            callback=read_more_callback
        ),
        Transition(
            next_state="ask_template",
            condition=_change_from_confirmation_to_ask_template,
            callback=confirmation_success_callback
        ),
        Transition(
            next_state="confirm_shell_exec",
            condition=_change_from_confirmation_to_confirm_shell_exec
        )
        
    ]

    def on_start(self, context: dict) -> dict:
        template = context["template"]
        location = context["location"]
        extra_parameters = context["extra_parameters"]

        context["n_lines_warning"] = 0
        context["read_more_link"] = context["template"].read_more_link

        confirmed, n_lines = DownloadQuestions.confirm_download(
            template=template,
            location=Path(location).resolve(),
            read_more_option=context["read_more_link"] != "",
            **extra_parameters
        )

        context.update(dict(
            n_lines=n_lines,
            confirmed=confirmed
        ))
        context["extra_parameters"]["confirm_shell_exec"] = False

        return context
