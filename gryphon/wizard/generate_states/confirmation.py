import logging
from ..wizard_text import Text
from ..questions import GenerateQuestions
from ..functions import display_template_information, erase_lines
from ...fsm import Transition, State, negate_condition
from ...constants import NO

logger = logging.getLogger('gryphon')


def _condition_confirmation_to_install(context: dict) -> bool:
    return context["confirmation_response"] == NO


def _callback_confirmation_to_install(context: dict) -> dict:
    erase_lines(n_lines=len(context["extra_parameters"]) + 2 + context["n_lines"])
    return context


class Confirmation(State):
    name = "confirmation"
    transitions = [
        Transition(
            next_state="install",
            condition=negate_condition(_condition_confirmation_to_install)
        ),
        Transition(
            next_state="ask_template",
            condition=_condition_confirmation_to_install,
            callback=_callback_confirmation_to_install
        )
    ]

    def on_start(self, context: dict) -> dict:
        context["template"] = context["templates"][context["template_name"]]
        context["n_lines"] = display_template_information(context["template"])

        context["extra_parameters"] = {}
        if len(context["template"].arguments):
            logger.info(Text.generate_ask_extra_parameters)
            context["extra_parameters"] = GenerateQuestions.ask_extra_arguments(context["template"].arguments)

        context["confirmation_response"] = GenerateQuestions.confirm_generate(
            template_name=context["template"].display_name,
            **context["extra_parameters"]
        )

        return context
