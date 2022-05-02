from ...fsm import State
from ...core.add import add as core_add
from ...constants import NAME


class AddLibrary(State):
    name = "add_library"
    transitions = []

    def on_start(self, context: dict) -> dict:
        lib = context["chosen_option"][NAME]

        core_add(
            library_name=lib,
            version=context['lib_version'] if 'lib_version' in context else None

        )
        return context
