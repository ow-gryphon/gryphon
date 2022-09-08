from ...fsm import State
from ...core.init import init as core_init
from ...constants import NB_EXTENSIONS, NB_STRIP_OUT, PRE_COMMIT_HOOKS


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
            install_nb_strip_out=NB_STRIP_OUT in context["selected_addons"],
            install_pre_commit_hooks=PRE_COMMIT_HOOKS in context["selected_addons"],
            install_nbextensions=NB_EXTENSIONS in context["selected_addons"],
            **extra_parameters
        )

        return context
