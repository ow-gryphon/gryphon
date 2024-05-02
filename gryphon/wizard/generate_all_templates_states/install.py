from ...fsm import State
from ...core import generate as core_generate
# from ...core.download import download as core_download
from ...core.registry.versioned_template import VersionedTemplate
from ...constants import DOWNLOAD, GENERATE, LATEST
import logging

logger = logging.getLogger('gryphon')


class Install(State):
    name = "install"
    transitions = []

    def on_start(self, context: dict) -> dict:
    
        # template = context["template"]
        #
        # if template.command == DOWNLOAD:
        #
        #     # This should never be reached, as a different path of the finite state machine should have been reached for DOWNLOAD templates
        #     raise ValueError("An error has occured. Please notify the Gryphon support team")
        #
        # else:
        #
        #     core_generate(
        #         template=context["template"],
        #         **context["extra_parameters"]
        #     )

        for template in context["templates"]:

            if isinstance(template, VersionedTemplate):

                context["template"] = template[LATEST]

            else:
                context["template"] = template

            context["extra_parameters"] = {}

            if context["template"].command == GENERATE:

                core_generate(
                    template=context["template"],
                    **context["extra_parameters"]
                )

        return context
