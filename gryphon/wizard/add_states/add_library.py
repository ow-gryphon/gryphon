from ...constants import NAME
from ...core.add import add as core_add
from ...fsm import State


class AddLibrary(State):
    name = "add_library"
    transitions = []

    def on_start(self, context: dict) -> dict:
        for option in context["chosen_option"]:
            lib = option[NAME]

            core_add(
                library_name=lib,
                version=context['lib_version'] if 'lib_version' in context else None

            )
        return context
