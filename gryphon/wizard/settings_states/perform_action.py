import logging
from ..functions import erase_lines
from ...fsm import State, Transition

logger = logging.getLogger('gryphon')


def back_to_previous(history, **kwargs):
    history.pop()
    erase_lines(**kwargs)


def _condition_from_perform_action_to_change_python_version(context: dict) -> bool:
    return context["history"][0] == "change_python_version"


def _condition_from_perform_action_to_new_template(context: dict) -> bool:
    return context["history"][0] == "new_template"


def _condition_from_perform_action_to_change_env_manager(context: dict) -> bool:
    return context["history"][0] == "change_env_manager"


def _condition_from_perform_action_to_restore_default_registry(context: dict) -> bool:
    return \
        len(context["history"]) >= 2 \
        and context["history"][0] == "registry_options"\
        and "restore_default_registry" in context["history"][1]


def _condition_from_perform_action_to_remove_registry(context: dict) -> bool:
    return \
        len(context["history"]) >= 2 \
        and context["history"][0] == "registry_options"\
        and "remove_registry" == context["history"][1]


def _condition_from_perform_action_to_add_remote_registry(context: dict) -> bool:
    return \
        len(context["history"]) >= 2 \
        and context["history"][0] == "registry_options"\
        and "add" in context["history"][1] \
        and "remote" in context["history"][1]


def _condition_from_perform_action_to_add_local_registry(context: dict) -> bool:
    return \
        len(context["history"]) >= 2 \
        and context["history"][0] == "registry_options"\
        and "add" in context["history"][1] \
        and "local" in context["history"][1]


def _condition_from_perform_action_to_restore_defaults(context: dict) -> bool:
    return context["history"][0] == "restore_defaults"


def _callback_from_perform_action_to_change_python_version(context: dict) -> dict:
    return context


class PerformAction(State):
    name = "perform_action"
    transitions = [
        Transition(
            next_state="change_python_version",
            condition=_condition_from_perform_action_to_change_python_version
        ),
        Transition(
            next_state="new_template",
            condition=_condition_from_perform_action_to_new_template
        ),
        Transition(
            next_state="change_env_manager",
            condition=_condition_from_perform_action_to_change_env_manager
        ),
        Transition(
            next_state="restore_defaults",
            condition=_condition_from_perform_action_to_restore_defaults
        ),


        Transition(
            next_state="restore_default_registry",
            condition=_condition_from_perform_action_to_restore_default_registry
        ),
        Transition(
            next_state="add_remote_registry",
            condition=_condition_from_perform_action_to_add_remote_registry
        ),
        Transition(
            next_state="add_local_registry",
            condition=_condition_from_perform_action_to_add_local_registry
        ),
        Transition(
            next_state="remove_registry",
            condition=_condition_from_perform_action_to_remove_registry
        )
    ]

    def on_start(self, context: dict) -> dict:

        return context
