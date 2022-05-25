from glob import glob
from pathlib import Path

from ..questions import HandoverQuestions
from ...constants import BACK, CHANGE_LIMIT
from ...fsm import State, Transition
from ...wizard.functions import erase_lines
from ...core.settings import SettingsManager


def _condition_check_files_to_ask_folder(context):
    return context["response"] == BACK


def _callback_check_files_to_ask_folder(context):
    erase_lines(n_lines=2)
    erase_lines(n_lines=context["extra_lines"])
    context.pop("extra_lines")
    return context


def _callback_ask_folder_ask_again_invalid_gryphon(context):
    return context


def list_files(path):
    base_path = str(path)
    pattern = str(path / '**')

    return [
        f.split(base_path)[1][1:]
        for f in glob(pattern, recursive=True)
        if Path(f).is_file() and ".git" not in f and "__pycache__" not in f
    ]


def get_large_file_list(path):
    file_list = list_files(path)

    file_sizes = {
        f: Path().stat().st_size / 10e6
        for f in file_list
    }

    limit = SettingsManager.get_handover_file_size_limit()

    large_file_list = list(filter(lambda x: x[1] > limit, file_sizes.items()))

    return large_file_list


class CheckLargeFiles(State):
    name = "check_large_files"
    transitions = [
        Transition(
            next_state="ask_folder",
            condition=_condition_check_files_to_ask_folder,
            callback=_callback_check_files_to_ask_folder
        )
    ]

    def on_start(self, context: dict) -> dict:
        # check for large files
        large_file_list = get_large_file_list(context["location"])
        has_large_files = len(large_file_list) > 0

        if has_large_files:
            context["response"] = HandoverQuestions.ask_large_files()
            if context["response"] != CHANGE_LIMIT:
                pass
            else:
                # change limit and return to the same state
                return context

        return context

# TODO: Restore defaults is not working
# TODO: copiando .git folder to em casos
