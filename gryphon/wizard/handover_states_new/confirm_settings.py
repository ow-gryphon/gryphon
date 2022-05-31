from ..questions.handover_questions import HandoverQuestions
from ...constants import BACK, NO, YES
from ...core.common_operations import list_files
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
            logger.warning(f"   - {file[:40].ljust(40)}\t{size:.2f} MB")

        logger.warning("")

    @classmethod
    def handle_file_sizes(cls, context):
        limit = SettingsManager.get_handover_file_size_limit()
        include_large_files = SettingsManager.get_handover_include_large_files()

        file_sizes = cls.get_file_sizes(context["location"])
        large_file_list = cls.filter_large_files(file_sizes, limit)
        has_large_files = len(large_file_list) > 0

        context["file_list"] = list(file_sizes.keys())
        context["excluded_files"] = []

        if has_large_files:
            cls.print_large_file_list(large_file_list, limit)
            context["extra_lines"] = len(large_file_list) + 5

            if include_large_files:
                logger.warning(
                    "Despite being larger than the limit set this files will be included on the zip package.")
            else:
                context["excluded_files"] = list(large_file_list.keys())
                logger.warning(
                    f"The listed files will not be included in the zip package because they exceeded the size "
                    f"limit of {limit} MB.")
            logger.warning("")
        else:
            logger.warning(f"No large files that exceeded the size limit were found ({limit} MB).")
            context["extra_lines"] = 1

    @staticmethod
    def handle_gryphon_files(context):
        include_gryphon_files = SettingsManager.get_handover_include_gryphon_generated_files()

        rc_file = RCManager.get_rc_file(context["location"])
        files = RCManager.get_gryphon_files(logfile=rc_file)

        file_names = list(map(lambda x: x["path"], files))

        if not include_gryphon_files:
            # append
            context["excluded_files"].extend(file_names)

            # deduplicate
            context["excluded_files"] = list(set(context["excluded_files"]))

            if len(file_names):
                # there are gryphon generated files
                logger.warning("The template files created by Gryphon WILL NOT be included on the zip:")
                for f in file_names:
                    logger.warning(f"   - {f[:40].ljust(40)}")

                context["extra_lines"] += (1 + len(file_names))

            else:
                logger.warning("There aren't any Gryphon generated files on the current project.")
                context["extra_lines"] += 1

        else:
            if len(file_names):
                logger.warning("The template files created by Gryphon WILL be included on the zip:")

                for f in file_names:
                    logger.warning(f"   - {f[:40].ljust(40)}")

            context["extra_lines"] += (1 + len(file_names))

    def on_start(self, context: dict) -> dict:

        context.pop("response", None)

        self.handle_file_sizes(context)
        self.handle_gryphon_files(context)

        context["response"] = HandoverQuestions.confirm_to_proceed()

        return context

# TODO: get the settings from the gryphon_rc file if there is if not get from the
# TODO: put text wrapping on the wider lines
