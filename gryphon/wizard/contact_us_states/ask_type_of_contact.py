from ..functions import (
    BackSignal, erase_lines
)
from ..questions import ContactUsQuestions
from ...constants import BACK, FEEDBACK, REPORT_BUG
from ...core.feedback import feedback
from ...core.report_bug import report_bug
from ...fsm import Transition, State


def _condition_back(context: dict) -> bool:
    return context["type_of_contact"] == BACK


def _callback_back(_):
    erase_lines()
    raise BackSignal()


def _condition_bug(context: dict) -> bool:
    return context["type_of_contact"] == REPORT_BUG


def _callback_bug(context: dict) -> dict:
    report_bug()
    return context


def _condition_feedback(context: dict) -> bool:
    return context["type_of_contact"] == FEEDBACK


def _callback_feedback(context: dict) -> dict:
    feedback()
    return context


class AskTypeOfContact(State):
    name = "ask_category"
    transitions = [
        Transition(
            next_state="placeholder",
            condition=_condition_bug,
            callback=_callback_bug
        ),
        Transition(
            next_state="placeholder",
            condition=_condition_feedback,
            callback=_callback_feedback
        ),
        Transition(
            next_state="placeholder",
            condition=_condition_back,
            callback=_callback_back
        )
    ]

    def on_start(self, context: dict) -> dict:
        # raise ValueError("haha")
        context["type_of_contact"] = ContactUsQuestions.feedback_or_bug()
        return context
