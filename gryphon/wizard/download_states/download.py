from ...fsm import State
from ...core.download import download as core_download

class Download(State):
    name = "download"
    transitions = []

    def on_start(self, context: dict) -> dict:
        template = context["template"]
        location = context["location"]
        extra_parameters = context["extra_parameters"]

        core_download(
            template=template,
            location=location,
            **extra_parameters
        )

        return context
