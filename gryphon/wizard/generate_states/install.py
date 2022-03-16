from ...fsm import State
from ...core import generate as core_generate


class Install(State):
    name = "install"
    transitions = []

    def on_start(self, context: dict) -> dict:
        core_generate(
            template_path=context["template"].path,
            requirements=context["template"].dependencies,
            **context["extra_parameters"]
        )

        return context
