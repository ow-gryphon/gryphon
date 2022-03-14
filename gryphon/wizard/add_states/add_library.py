from ...fsm import State
from ...core.add import add as core_add
from ...constants import NAME


class AddLibrary(State):
    name = "add_library"
    transitions = []

    def on_start(self, context: dict) -> dict:
        core_add(
            library_name=context["chosen_option"][NAME]
        )
        return context
