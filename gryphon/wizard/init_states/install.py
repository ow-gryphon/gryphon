from ...fsm import State
from ...core.init import init as core_init


class Install(State):
    name = "install"
    transitions = []

    def on_start(self, context: dict) -> dict:
        template = context["template"]
        location = context["location"]
        chosen_version = context["chosen_version"]
        extra_parameters = context["extra_parameters"]

        core_init(
            template=template,
            location=location,
            python_version=chosen_version,
            **extra_parameters
        )

        return context
