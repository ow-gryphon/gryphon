from ...fsm import State
from ...core.add import add as core_add
from ...constants import NAME


class AddLibrary(State):
    name = "add_library"
    transitions = []

    def on_start(self, context: dict) -> dict:
        lib = context["chosen_option"][NAME]
        if "lib_version" in context:
            lib = f"{lib}=={context['lib_version']}"

        core_add(
            library_name=lib
        )
        return context
