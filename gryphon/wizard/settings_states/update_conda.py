import logging
from ...fsm import State, Transition
from ...core.operations.environment_manager_operations import EnvironmentManagerOperations
from ...constants import YES, SUCCESS


logger = logging.getLogger('gryphon')


#####
def _condition_from_change_env_manager_to_end(context: dict) -> bool:
    return context["confirmation_option"] == YES


def _callback_from_change_env_manager_to_end(context: dict) -> dict:
    logger.log(SUCCESS, "Conda updated successfully")

    context["history"] = []
    print("\n")
    return context


####
def _condition_from_change_env_manager_to_ask_option(_: dict) -> bool:
    return True


class UpdateConda(State):
    name = "update_conda"
    transitions = [
        Transition(
            next_state="ask_option",
            condition=_condition_from_change_env_manager_to_ask_option,
            callback=_callback_from_change_env_manager_to_end
        )
    ]

    def on_start(self, context: dict) -> dict:
        logger.info("Updating conda. This may take several minutes...")
        EnvironmentManagerOperations.update_conda()
        return context
