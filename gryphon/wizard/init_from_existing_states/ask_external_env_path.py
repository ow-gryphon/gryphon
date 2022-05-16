from ...fsm import State, Transition
from ...wizard.questions import InitFromExistingQuestions


class AskExternalEnvPath(State):
    name = "ask_external_env_path"
    transitions = [
        Transition(
            next_state="install",
            condition=lambda context: True
        )
    ]

    def on_start(self, context: dict) -> dict:
        context["external_env_path"] = InitFromExistingQuestions.ask_external_env_path()

        return context
