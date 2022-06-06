from ...core.handover import handover
from ...core.operations import RCManager, SettingsManager
from ...fsm import State


class CreateHandoverPackage(State):
    name = "create_handover_package"
    transitions = []

    def on_start(self, context: dict) -> dict:
        # check for large files
        logfile = RCManager.get_rc_file(context["location"])
        handover(
            path=context["location"],
            output_path=context["output_file"],
            gryphon_exclusion_list=context["excluded_files_gryphon"],
            large_files_exclusion_list=context["excluded_files_size"],
            file_list=context["file_list"],
            configs=dict(
                keep_gryphon_files=RCManager.get_handover_include_gryphon_generated_files(logfile),
                file_size_limit=SettingsManager.get_handover_file_size_limit()
            )
        )
        return context
