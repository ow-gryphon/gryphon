import logging
import os
import platform
from pathlib import Path

from ..init_from_existing import init_from_existing
from ..functions import erase_lines, BackSignal
from ..questions import InitQuestions
from ...constants import YES, NO, READ_MORE, CHANGE_LOCATION, SUCCESS, BACK
from ...fsm import State, Transition, HaltSignal

logger = logging.getLogger('gryphon')


def confirmation_success_callback(context: dict) -> dict:
    n_lines = context["n_lines"]
    ask_again = context["n_lines_ask_again"] if "n_lines_ask_again" in context else 0

    erase_lines(n_lines=n_lines + 2 + context["n_lines_warning"] + ask_again)
    return context


def ask_location_again_callback(context: dict) -> dict:
    n_lines = context["n_lines"]
    ask_again = context["n_lines_ask_again"] if "n_lines_ask_again" in context else 0

    erase_lines(n_lines=n_lines + 2 + context["n_lines_warning"] + ask_again)
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


def _change_from_confirmation_to_install(context: dict) -> bool:
    confirmed = context["confirmed"]
    return confirmed == YES


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
            next_state="select_addons",
            condition=_change_from_confirmation_to_ask_template,
            callback=confirmation_success_callback
        ),
        Transition(
            next_state="install",
            condition=_change_from_confirmation_to_install
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
        )
    ]

    def __init__(self, registry):
        self.registry = registry

    def on_start(self, context: dict) -> dict:
        template = context["template"]
        location = context["location"]
        extra_parameters = context["extra_parameters"]

        context["n_lines_warning"] = 0
        path = Path.cwd() / location

        if path.is_dir():
            context["n_lines_warning"] = 2

            def is_empty(x): return not os.listdir(x)

            if is_empty(path):
                # empty
                logger.warning("\nWARNING: The selected folder already exists.")
            else:
                # not empty
                logger.warning("\nWARNING: The selected folder is not empty.")
                want_to_go_to_init_from_existing = InitQuestions.ask_init_from_existing()
                context["n_lines_warning"] += 1

                if want_to_go_to_init_from_existing:
                    ask_again = context["n_lines_ask_again"] if "n_lines_ask_again" in context else 0
                    erase_lines(n_lines=4 + context["n_lines_warning"] + ask_again)

                    logger.log(SUCCESS, "Creating Gryphon project from the existing folder")
                    result = init_from_existing(None, self.registry)

                    if result == BACK:
                        raise BackSignal()
                    else:
                        raise HaltSignal()

        context["read_more_link"] = context["template"].read_more_link

        confirmed, n_lines = InitQuestions.confirm_init(
            template=template,
            location=Path(location).resolve(),
            read_more_option=context["read_more_link"] is not None,
            addons=context["selected_addons"],
            **extra_parameters
        )

        context.update(dict(
            n_lines=n_lines,
            confirmed=confirmed
        ))
        return context
