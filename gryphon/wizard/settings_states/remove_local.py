import logging

from ..functions import erase_lines
from ..questions import SettingsQuestions
from ...constants import YES, SUCCESS, BACK
from ...core.operations.settings import SettingsManager
from ...fsm import State, Transition, negate_condition

logger = logging.getLogger('gryphon')


def back_to_previous(history, **kwargs):
    history.pop()
    erase_lines(**kwargs)


#####

def _callback_from_change_env_manager_to_end(context: dict) -> dict:
    SettingsManager.remove_local_template(context["chosen_template"])
    logger.log(SUCCESS, "Local template successfully removed")

    context["history"] = []
    print("\n")
    return context


####
def _condition_from_change_env_manager_to_ask_option(context: dict) -> bool:
    return context["chosen_template"] == BACK


def _callback_from_from_change_env_manager_to_ask_option(context: dict) -> dict:
    # remove 2 entries from history
    back_to_previous(context["history"], n_lines=1)
    back_to_previous(context["history"], n_lines=1)
    return context


class RemoveLocal(State):
    name = "remove_local"
    transitions = [
        Transition(
            next_state="ask_option",
            condition=_condition_from_change_env_manager_to_ask_option,
            callback=_callback_from_from_change_env_manager_to_ask_option
        ),
        Transition(
            next_state="ask_option",
            condition=negate_condition(_condition_from_change_env_manager_to_ask_option),
            callback=_callback_from_change_env_manager_to_end
        )
    ]

    def on_start(self, context: dict) -> dict:
        choices = SettingsManager.get_local_templates()
        context["chosen_template"] = SettingsQuestions.ask_witch_local_template(choices)
        return context
