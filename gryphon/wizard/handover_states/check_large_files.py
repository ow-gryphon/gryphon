from ..questions import HandoverQuestions
from ...constants import BACK, CHANGE_LIMIT, YES, NO
from ...core.common_operations import list_files
from ...core.settings import SettingsManager
from ...fsm import State, Transition
from ...wizard.functions import erase_lines


def _condition_check_files_to_ask_folder(context):
    return "response" in context and context["response"] == BACK


def _condition_check_files_to_change_limits(context):
    return "response" in context and context["response"] == CHANGE_LIMIT


def _condition_check_files_to_do_stuff(context):
    return "response" not in context


def _callback_check_files_to_ask_folder(context):
    erase_lines(n_lines=2)
    erase_lines(n_lines=context["extra_lines"])
    context.pop("extra_lines")
    return context


def _callback_ask_folder_ask_again_invalid_gryphon(context):
    return context


def get_file_sizes(path):
    file_list = list_files(path)

    file_sizes = {
        f: (path / f).stat().st_size / 1e6
        for f in file_list
    }
    return file_sizes


def filter_large_files(file_sizes):
    limit = SettingsManager.get_handover_file_size_limit()

    large_file_list = dict(filter(lambda x: x[1] > limit, file_sizes.items()))

    return large_file_list


class CheckLargeFiles(State):
    name = "check_large_files"
    transitions = [
        Transition(
            next_state="ask_folder",
            condition=_condition_check_files_to_ask_folder,
            callback=_callback_check_files_to_ask_folder
        ),
        Transition(
            next_state="change_size_limits",
            condition=_condition_check_files_to_change_limits,
        ),
        Transition(
            next_state="do_stuff",
            condition=_condition_check_files_to_do_stuff
        )
    ]

    def on_start(self, context: dict) -> dict:
        # check for large files
        context.pop("response", None)
        file_sizes = get_file_sizes(context["location"])
        large_file_list = filter_large_files(file_sizes)
        has_large_files = len(large_file_list) > 0

        if has_large_files:
            limit = SettingsManager.get_handover_file_size_limit()
            context["response"] = HandoverQuestions.ask_large_files(limit)
            if context["response"] != CHANGE_LIMIT:

                if context["response"] == YES:
                    context["excluded_files"] = []

                elif context["response"] == NO:
                    context["excluded_files"] = list(large_file_list.keys())

            else:
                context["file_sizes"] = file_sizes

        return context
