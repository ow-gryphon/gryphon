from ..questions import AddQuestions
from ...constants import NAME
from ...fsm import State, Transition


class TypeLibraryName(State):
    name = "type_library_name"
    transitions = [
        Transition(
            next_state="confirmation",
            condition=lambda context: True
        )
    ]

    def on_start(self, context: dict) -> dict:
        context["chosen_option"] = {NAME: AddQuestions.get_lib_via_keyboard()}
        return context
