import logging

from ..functions import erase_lines
from ..questions import SettingsQuestions
from ...constants import (BACK, YES, SUCCESS)
from ...core.operations import SettingsManager
from ...fsm import State, Transition, negate_condition

logger = logging.getLogger('gryphon')


def back_to_previous(history, **kwargs):
    history.pop()
    erase_lines(**kwargs)


#####
def _condition_from_add_local_registry_to_end(context: dict) -> bool:
    return context["registry_name"] == YES


def _callback_from_add_local_registry_to_end(context: dict) -> dict:
    manager = SettingsManager()
    result = SettingsQuestions.confirm_remove_registry()
    if result == YES:
        manager.remove_template_registry(context["registry_name"])
        logger.log(SUCCESS, f'Successfully removed registry {context["registry_name"]}.')
    else:
        back_to_previous(context["history"], n_lines=2)
        back_to_previous(context["history"], n_lines=1)
        return context

    context["history"] = []
    print("\n")
    return context


#####
def _condition_from_add_local_registry_to_previous(context: dict) -> bool:
    return context["registry_name"] == BACK


def _callback_from_from_add_local_registry_to_previous(context: dict) -> dict:
    # remove 2 entries from history
    back_to_previous(context["history"], n_lines=0)
    back_to_previous(context["history"])
    return context


class RemoveRegistry(State):
    name = "remove_registry"
    transitions = [
        Transition(
            next_state="ask_option",
            condition=negate_condition(_condition_from_add_local_registry_to_previous),
            callback=_callback_from_add_local_registry_to_end
        ),
        Transition(
            next_state="ask_option",
            condition=_condition_from_add_local_registry_to_previous,
            callback=_callback_from_from_add_local_registry_to_previous
        )
    ]

    def on_start(self, context: dict) -> dict:
        manager = SettingsManager()
        context["registries"] = manager.list_template_registries()
        context["registry_name"] = SettingsQuestions.ask_which_registry_to_remove(context["registries"])

        return context
