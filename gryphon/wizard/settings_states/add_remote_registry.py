import logging
from ..functions import erase_lines
from ..questions import SettingsQuestions
from ...fsm import State, Transition
from ...constants import NO
from ...constants import (YES, SUCCESS)
from ...core.settings import SettingsManager


logger = logging.getLogger('gryphon')


def back_to_previous(history, **kwargs):
    history.pop()
    erase_lines(**kwargs)


#####
def _condition_from_add_remote_registry_to_end(context: dict) -> bool:
    return context["confirmation_option"] == YES


def _callback_from_add_remote_registry_to_end(context: dict) -> dict:
    manager = SettingsManager()
    manager.add_git_template_registry(
        registry_name=context["registry_name"],
        registry_repo=context["url"]
    )
    logger.log(SUCCESS, f'Successfully added registry {context["registry_name"]}.')

    context["history"] = []
    print("\n")
    return context


####
def _condition_from_add_remote_registry_to_ask_option(context: dict) -> bool:
    return context["confirmation_option"] == NO


def _callback_from_from_add_remote_registry_to_ask_option(context: dict) -> dict:
    # remove 2 entries from history
    back_to_previous(context["history"], n_lines=2)
    back_to_previous(context["history"], n_lines=2)
    return context


class AddRemoteRegistry(State):
    name = "add_remote_registry"
    transitions = [
        Transition(
            next_state="ask_option",
            condition=_condition_from_add_remote_registry_to_ask_option,
            callback=_callback_from_from_add_remote_registry_to_ask_option
        ),
        Transition(
            next_state="ask_option",
            condition=_condition_from_add_remote_registry_to_end,
            callback=_callback_from_add_remote_registry_to_end
        )
    ]

    def on_start(self, context: dict) -> dict:
        context["registry_name"] = SettingsQuestions.ask_registry_name()
        context["url"] = SettingsQuestions.ask_git_url()
        context["confirmation_option"] = SettingsQuestions.confirm_registry_addition(context["registry_name"])
        return context
