from ...fsm import State
from ...core.download import download as core_download


class Download(State):
    name = "download"
    transitions = []

    def on_start(self, context: dict) -> dict:
        template = context["template"]
        
        if 'location' not in context.keys():
            location = context['template'].name
        else:
            location = context["location"]
        extra_parameters = context["extra_parameters"]

        core_download(
            template=template,
            location=location,
            **extra_parameters
        )

        return context
