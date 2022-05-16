from ...core.init_from_existing import check_for_environment
from ...fsm import State, Transition
from ...wizard.questions import InitFromExistingQuestions


def _condition_ask_use_existing(context: dict) -> bool:
    return context["is_there_any_existing_environment"]


def _condition_ask_point_external(context: dict) -> bool:
    return not context["is_there_any_existing_environment"]


class AskLocation(State):
    name = "ask_location"
    transitions = [
        Transition(
            next_state="ask_point_external",
            condition=_condition_ask_point_external
        ),
        Transition(
            next_state="ask_use_existing",
            condition=_condition_ask_use_existing
        )
    ]

    def on_start(self, context: dict) -> dict:
        context["location"] = InitFromExistingQuestions.ask_existing_location()
        found_conda, found_venv, conda_path, venv_path = check_for_environment(context["location"])

        context["found_conda"], context["found_venv"] = found_conda, found_venv
        context["conda_path"], context["venv_path"] = conda_path, venv_path
        context["is_there_any_existing_environment"] = found_conda or found_venv

        return context
