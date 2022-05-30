import logging
from ..functions import erase_lines
from ..questions import SettingsQuestions
from ...fsm import State, Transition
from ...constants import NO
from ...constants import (YES, SUCCESS)
from ...core.operations import SettingsManager


logger = logging.getLogger('gryphon')


def back_to_previous(history, **kwargs):
    history.pop()
    erase_lines(**kwargs)


#####
def _condition_from_change_env_manager_to_end(context: dict) -> bool:
    return context["confirmation_option"] == YES


def _callback_from_change_env_manager_to_end(context: dict) -> dict:
    manager = SettingsManager()
    manager.change_environment_manager(context["actual_selection"].lower())
    logger.log(SUCCESS, f'Environment management successfully changed to {context["actual_selection"]}')

    context["history"] = []
    print("\n")
    return context


####
def _condition_from_change_env_manager_to_ask_option(context: dict) -> bool:
    return context["confirmation_option"] == NO


def _callback_from_from_change_env_manager_to_ask_option(context: dict) -> dict:
    # remove 2 entries from history
    back_to_previous(context["history"], n_lines=1)
    back_to_previous(context["history"], n_lines=1)
    return context


class ChangeEnvManager(State):
    name = "change_env_manager"
    transitions = [
        Transition(
            next_state="ask_option",
            condition=_condition_from_change_env_manager_to_ask_option,
            callback=_callback_from_from_change_env_manager_to_ask_option
        ),
        Transition(
            next_state="ask_option",
            condition=_condition_from_change_env_manager_to_end,
            callback=_callback_from_change_env_manager_to_end
        )
    ]

    def on_start(self, context: dict) -> dict:
        context["confirmation_option"] = SettingsQuestions.confirm_change_env_manager(context["actual_selection"])
        return context
