from ...core.handover import handover
from ...fsm import State


class CreateHandoverPackage(State):
    name = "create_handover_package"
    transitions = []

    def on_start(self, context: dict) -> dict:
        # check for large files
        handover(
            path=context["location"],
            output_path=context["output_file"],
            exclusion_list=context["excluded_files"],
            file_list=context["file_list"]
        )
        return context
