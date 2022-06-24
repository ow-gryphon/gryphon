import logging

from ..functions import erase_lines
from ..questions import SettingsQuestions
from ...constants import NO
from ...constants import (
    YES, SUCCESS
)
from ...core.operations import SettingsManager
from ...fsm import State, Transition

logger = logging.getLogger('gryphon')


def back_to_previous(history, **kwargs):
    history.pop()
    erase_lines(**kwargs)


#####
def _condition_from_add_local_registry_to_end(context: dict) -> bool:
    return context["confirmation_option"] == YES


def _callback_from_add_local_registry_to_end(context: dict) -> dict:
    manager = SettingsManager()
    manager.add_local_template_registry(
        registry_name=context["registry_name"],
        registry_path=context["path"]
    )
    logger.log(SUCCESS, f'Successfully added registry {context["registry_name"]}.')

    context["history"] = []
    print("\n")
    return context


####
def _condition_from_add_local_registry_to_ask_option(context: dict) -> bool:
    return context["confirmation_option"] == NO


def _callback_from_from_add_local_registry_to_ask_option(context: dict) -> dict:
    # remove 2 entries from history
    back_to_previous(context["history"], n_lines=2)
    back_to_previous(context["history"], n_lines=2)
    return context


class AddLocalRegistry(State):
    name = "add_local_registry"
    transitions = [
        Transition(
            next_state="ask_option",
            condition=_condition_from_add_local_registry_to_ask_option,
            callback=_callback_from_from_add_local_registry_to_ask_option
        ),
        Transition(
            next_state="ask_option",
            condition=_condition_from_add_local_registry_to_end,
            callback=_callback_from_add_local_registry_to_end
        )
    ]

    def on_start(self, context: dict) -> dict:
        context["registry_name"] = SettingsQuestions.ask_registry_name()
        context["path"] = SettingsQuestions.ask_local_path()
        context["confirmation_option"] = SettingsQuestions.confirm_registry_addition(context["registry_name"])

        return context
