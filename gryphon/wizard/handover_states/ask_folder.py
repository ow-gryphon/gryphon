from ..functions import erase_lines, BackSignal
from ..questions import HandoverQuestions
from ...constants import GRYPHON_RC, BACK
from ...fsm import State, Transition
from ...logger import logger


def _condition_ask_folder_ask_again(context):
    return not context["location"].is_dir()


def _condition_ask_folder_ask_again_invalid_gryphon(context):
    return context["location"].is_dir() and not (context["location"] / GRYPHON_RC).is_file()


def _condition_ask_folder_ask_again_check_large_files(context):
    return context["location"].is_dir() and (context["location"] / GRYPHON_RC).is_file()


def _callback_ask_folder_ask_again(context):
    AskFolder.handle_invalid_path(context)
    return context


def _callback_ask_folder_ask_again_invalid_gryphon(context):
    AskFolder.handle_invalid_gryphon_path(context)
    return context


class AskFolder(State):
    name = "ask_folder"
    transitions = [
        Transition(
            next_state="ask_folder",
            condition=_condition_ask_folder_ask_again,
            callback=_callback_ask_folder_ask_again
        ),
        Transition(
            next_state="ask_folder",
            condition=_condition_ask_folder_ask_again_invalid_gryphon,
            callback=_callback_ask_folder_ask_again_invalid_gryphon
        ),
        Transition(
            next_state="confirm_settings",
            condition=_condition_ask_folder_ask_again_check_large_files,
        )
    ]

    @staticmethod
    def handle_invalid_path(context):
        erase_lines(n_lines=2)
        erase_lines(n_lines=context["extra_lines"])
        logger.warning(f'Provided folder does not exists \"{context["location"]}\". Try again.\n')
        context["extra_lines"] = 1

    @staticmethod
    def handle_invalid_gryphon_path(context):
        erase_lines(n_lines=2)
        erase_lines(n_lines=context["extra_lines"])
        logger.warning(f'Provided folder is not a valid Gryphon project \"{context["location"]}\". Try again.\n')
        context["extra_lines"] = 1

    def on_start(self, context: dict) -> dict:
        if "extra_lines" not in context:
            context["extra_lines"] = 0

        context["location"] = HandoverQuestions.ask_project_folder()
        if context["location"] == BACK:
            erase_lines(n_lines=2)
            raise BackSignal()

        return context
