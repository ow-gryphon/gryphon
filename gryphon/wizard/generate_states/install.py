from ...fsm import State
from ...core import generate as core_generate
# from ...core.download import download as core_download
from ...constants import DOWNLOAD
import logging

logger = logging.getLogger('gryphon')


class Install(State):
    name = "install"
    transitions = []

    def on_start(self, context: dict) -> dict:
    
        template = context["template"]
        
        if template.command == DOWNLOAD:
            
            # This should never be reached, as a different path of the finite state machine should have been reached for DOWNLOAD templates
            raise ValueError("An error has occured. Please notify the Gryphon support team")
        
        else:
            core_generate(
                template=context["template"],
                **context["extra_parameters"]
            )

        return context
