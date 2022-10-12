from ..functions import erase_lines
from ..questions import AddQuestions
from ...constants import NAME, BACK
from ...fsm import State, Transition, negate_condition


def _condition_back(context):
    return BACK in map(lambda x: x[NAME], context["chosen_option"])


def _callback_back(context):
    erase_lines()
    return context


class TypeLibraryName(State):
    name = "type_library_name"
    transitions = [
        Transition(
            next_state="confirmation",
            condition=negate_condition(_condition_back)
        ),
        Transition(
            next_state="ask_option",
            condition=_condition_back,
            callback=_callback_back
        )
    ]

    def on_start(self, context: dict) -> dict:
        context["chosen_option"] = [
            {NAME: lib}
            for lib in AddQuestions.get_lib_via_keyboard().split(" ")
            if len(lib)
        ]
        return context
