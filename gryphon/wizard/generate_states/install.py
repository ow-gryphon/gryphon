from ...fsm import State
from ...core import generate as core_generate
from ...core.download import download as core_download
from ...constants import DOWNLOAD


class Install(State):
    name = "install"
    transitions = []

    def on_start(self, context: dict) -> dict:
    
        template = context["template"]
        
        if template.command == DOWNLOAD:
            core_download(
                template=template,
                location=template.name
            )
        
        else:
            core_generate(
                template=context["template"],
                **context["extra_parameters"]
            )

        return context
