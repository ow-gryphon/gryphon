from textwrap import wrap

from ..questions.handover_questions import HandoverQuestions
from ...constants import BACK, NO, YES
from ...core.common_operations import list_files
from ...core.handover import get_output_file_name
from ...core.operations import SettingsManager, RCManager
from ...fsm import State, Transition
from ...logger import logger
from ...wizard.functions import erase_lines


def _condition_check_files_to_ask_folder(context):
    return "response" in context and context["response"] == BACK


def _condition_check_files_to_change_settings(context):
    return "response" in context and context["response"] == NO


def _condition_check_files_to_do_stuff(context):
    return "response" in context and context["response"] == YES


def _callback_check_files_to_ask_folder(context):
    erase_lines(n_lines=2)
    erase_lines(n_lines=context["extra_lines"])
    context.pop("extra_lines")
    return context


def _callback_ask_folder_ask_again_invalid_gryphon(context):
    return context


class ConfirmSettings(State):
    name = "confirm_settings"
    transitions = [
        Transition(
            next_state="ask_folder",
            condition=_condition_check_files_to_ask_folder,
            callback=_callback_check_files_to_ask_folder
        ),
        Transition(
            next_state="change_settings",
            condition=_condition_check_files_to_change_settings,
        ),
        Transition(
            next_state="create_handover_package",
            condition=_condition_check_files_to_do_stuff
        )
    ]

    @staticmethod
    def get_file_sizes(path):
        file_list = list_files(path)

        file_sizes = {
            f: (path / f).stat().st_size / 1e6
            for f in file_list
        }
        return file_sizes

    @staticmethod
    def filter_large_files(file_sizes, limit):
        large_file_list = dict(filter(lambda x: x[1] > limit, file_sizes.items()))

        return large_file_list

    @staticmethod
    def print_large_file_list(large_file_list, limit):
        logger.warning("")
        logger.warning(f"Files that exceeded the size limit ({limit} MB):")
        for file, size in large_file_list.items():
            logger.warning(f"   - {str(file)[:60].ljust(40)}\t{size:.2f} MB")

        logger.warning("")

    @classmethod
    def handle_file_sizes(cls, context):
        limit = SettingsManager.get_handover_file_size_limit()
        include_large_files = limit == float(0)

        logfile = RCManager.get_rc_file(context["location"])
        RCManager.set_handover_include_large_files(include_large_files, logfile=logfile)

        file_sizes = cls.get_file_sizes(context["location"])
        large_file_list = cls.filter_large_files(file_sizes, limit)
        has_large_files = len(large_file_list) > 0

        context["file_list"] = list(file_sizes.keys())
        context["excluded_files_size"] = []

        if has_large_files:

            if include_large_files:
                logger.warning("No files will be excluded from the zip file for being large.")
                context["extra_lines"] = 1
            else:
                cls.print_large_file_list(large_file_list, limit)
                context["extra_lines"] = len(large_file_list) + 3
                context["excluded_files_size"] = list(large_file_list.keys())

                for line in wrap(f"The listed files will not be included in the zip package because they exceeded "
                                 f"the size limit of {limit} MB.", width=100):
                    logger.warning(line)
                    context["extra_lines"] += 1

            logger.warning("")
            context["extra_lines"] += 1

        else:

            if not include_large_files:
                logger.warning("No files will be excluded from the zip file for being large.")
                context["extra_lines"] += 1
            else:
                logger.warning(f"No large files that exceeded the size limit were found ({limit} MB).")
                context["extra_lines"] = 1

    @staticmethod
    def handle_gryphon_files(context):
        rc_file = RCManager.get_rc_file(context["location"])
        try:
            include_gryphon_files = RCManager.get_handover_include_gryphon_generated_files(rc_file)
        except KeyError:
            include_gryphon_files = SettingsManager.get_handover_include_gryphon_generated_files()

        files = RCManager.get_gryphon_files(logfile=rc_file)

        file_names = list(map(lambda x: x["path"], filter(lambda x: "notebooks" in x["path"], files)))
        context["excluded_files_gryphon"] = []

        if not include_gryphon_files:
            context["excluded_files_gryphon"] = file_names

            if len(file_names):
                # there are gryphon generated files
                logger.warning("Some template files created by Gryphon WILL NOT be included on the zip:")
                logger.warning(f" - {len(file_names)} files inside the \"{context['location'] / 'notebooks'}\" folder.")
                context["extra_lines"] += 2

            else:
                logger.warning("There aren't any Gryphon generated files on the current project.")
                context["extra_lines"] += 1

        else:
            if len(file_names):
                logger.warning("Some template files created by Gryphon WILL be included on the zip:")
                logger.warning(f" - {len(file_names)} files inside the \"{context['location'] / 'notebooks'}\" folder.")
                context["extra_lines"] += 2

    def on_start(self, context: dict) -> dict:

        context.pop("response", None)

        self.handle_file_sizes(context)
        self.handle_gryphon_files(context)

        context["output_file"] = get_output_file_name(context["location"])
        context["response"], n_lines = HandoverQuestions.confirm_to_proceed(context["output_file"])
        context["extra_lines"] += n_lines - 1

        return context

# DONE: get the settings from the gryphon_rc file if there is if not get from the
# DONE: put text wrapping on the wider lines

# DONE: format timestamp on the zip name
# DONE: Create the file on the parent folder
# DONE: space separated values on add functionality

# DONE: Just consider to exclude gryphon files that are inside the notebooks
#  folder. Just display the amount of files inside the folder (not to print every
#  name as it could get very long)

# DONE: if user types 0 on the file limit don't consider the file size
# TODO: Have a logfile specifying how the zip was generated (configs and choices) placed on the parent folder
# DONE: show confirmation of file path
# DONE: CTRL + C as back on text fields
