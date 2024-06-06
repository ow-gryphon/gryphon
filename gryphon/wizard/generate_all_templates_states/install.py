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

        for counter, template in enumerate(context["templates"].values()):

            if isinstance(template, VersionedTemplate):

                context["template"] = template[LATEST]

            else:
                context["template"] = template

            context["extra_parameters"] = {}

            # if context["template"].command == GENERATE:

            core_generate(
                template=context["template"],
                install_dependencies=False,
                **context["extra_parameters"]
            )

            logger.info(f"Downloaded {counter+1} out of {len(context['templates'])} templates.")

        return context
