from ...constants import CONDA, VENV
from ...core.init_from_existing import init_from_existing
from ...fsm import State


class Install(State):
    name = "install"
    transitions = []

    def on_start(self, context: dict) -> dict:

        env = VENV
        path = None
        if "external_env_path" not in context:
            if context["found_conda"]:
                env = CONDA
                path = context["conda_path"]

            elif context["found_venv"]:
                env = VENV
                path = context["venv_path"]
        else:
            if context["found_conda"]:
                env = CONDA

            elif context["found_venv"]:
                env = VENV

            path = context["external_env_path"]

        init_from_existing(
            location=context["location"],
            env_manager=env,
            env_path=path,
            use_existing_environment=context["use_existing"]
        )

        return context
