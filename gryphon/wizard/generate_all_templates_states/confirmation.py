import json
import logging
# import os
# import platform

from ..functions import display_template_information, erase_lines
from ..questions import GenerateQuestions, CommonQuestions
from ..wizard_text import Text
from ...constants import (YES, NO, LATEST, USE_LATEST, ALWAYS_ASK, GENERATE_ALL_METHODOLOGY_TEMPLATES, CONFIG_FILE,
                          READ_MORE, DOWNLOAD, GENERATE, EMAIL_APPROVER, MMC_GITHUB_SETUP, MMC_GITHUB_SETUP_LINK)
from ...core.registry.versioned_template import VersionedTemplate
# from ...core.email_approver import email_approver
from ...fsm import Transition, State

logger = logging.getLogger('gryphon')


def _condition_confirmation_to_install(context: dict) -> bool:
    confirmed = context["confirmation_response"]
    command = context["template"].command
    return (confirmed == YES) and (command == GENERATE_ALL_METHODOLOGY_TEMPLATES)


# def _condition_confirmation_to_ask_template(context: dict) -> bool:
#     return context["confirmation_response"] == NO


# def _condition_confirmation_to_read_more(context: dict) -> bool:
#     return context["confirmation_response"] == READ_MORE


# def _condition_confirmation_to_email_approver(context: dict) -> bool:
#     return context["confirmation_response"] == EMAIL_APPROVER


# def _condition_confirmation_to_mmc_github_setup(context: dict) -> bool:
#     return context["confirmation_response"] == MMC_GITHUB_SETUP


def _callback_confirmation_to_install(context: dict) -> dict:
    erase_lines(n_lines=len(context["extra_parameters"]) + 3 + context["n_lines"])
    return context


# def _callback_confirmation_to_read_more(context: dict) -> dict:
#     if platform.system() == "Windows":
#         os.system(f'start {context["read_more_link"]}')
#     else:
#         os.system(f"""nohup xdg-open "{context["read_more_link"]}" """)
#         os.system(f"""rm nohup.out""")
#         erase_lines(n_lines=1)
#
#     erase_lines(n_lines=len(context["extra_parameters"]) + 1 + context["n_lines"])
#     return context


# def _callback_confirmation_to_email_approver(context: dict) -> dict:
#     email_approver(context["template"].approver, context["template"].repo_url)
#
#     erase_lines(n_lines=len(context["extra_parameters"]) + 2 + context["n_lines"])
#     return context


# def _callback_confirmation_to_mmc_github_setup(context: dict) -> dict:
#     if platform.system() == "Windows":
#         os.system(f'start {MMC_GITHUB_SETUP_LINK}')
#     else:
#         os.system(f"""nohup xdg-open "{MMC_GITHUB_SETUP_LINK}" """)
#         os.system(f"""rm nohup.out""")
#         erase_lines(n_lines=1)
#
#     erase_lines(n_lines=len(context["extra_parameters"]) + 2 + context["n_lines"])
#     return context


# Download templates
# def _change_from_confirmation_to_ask_project_info(context: dict) -> bool:
#     confirmed = context["confirmation_response"]
#     command = context["template"].command
#     return (confirmed == YES) and (command == DOWNLOAD) and not bool(context["template"].shell_exec)


# def _change_from_confirmation_to_confirm_shell_exec(context: dict) -> bool:
#     confirmed = context["confirmation_response"]
#     command = context["template"].command
#     return (confirmed == YES) and (command == DOWNLOAD) and bool(context["template"].shell_exec)


class Confirmation(State):
    name = "confirmation"
    transitions = [
        Transition(
            next_state="install",
            condition=_condition_confirmation_to_install
        ),
        # Transition(
        #     next_state="ask_template",
        #     condition=_condition_confirmation_to_ask_template,
        #     callback=_callback_confirmation_to_install
        # ),
        # Transition(
        #     next_state="confirmation",
        #     condition=_condition_confirmation_to_read_more,
        #     callback=_callback_confirmation_to_read_more
        # ),
        # Transition(
        #     next_state="confirm_shell_exec",
        #     condition=_change_from_confirmation_to_confirm_shell_exec
        # ),
        # Transition(
        #     next_state="ask_project_info",
        #     condition=_change_from_confirmation_to_ask_project_info
        # ),
        # Transition(
        #     next_state="confirmation",
        #     condition=_condition_confirmation_to_email_approver,
        #     callback=_callback_confirmation_to_email_approver
        # ),
        # Transition(
        #     next_state="confirmation",
        #     condition=_condition_confirmation_to_mmc_github_setup,
        #     callback=_callback_confirmation_to_mmc_github_setup
        # )
    ]

    def __init__(self, registry):
        self.templates = registry.get_templates(GENERATE)
        self.templates.update(registry.get_templates(DOWNLOAD))
        
        with open(CONFIG_FILE, "r+", encoding="utf-8") as f:
            self.settings = json.load(f)
        super().__init__()

    def on_start(self, context: dict) -> dict:
        # template = context["templates"][context["template_name"]]
        # if isinstance(template, VersionedTemplate):
        #
        #     if self.settings.get("template_version_policy") == USE_LATEST:
        #         context["template"] = template[LATEST]
        #
        #     elif self.settings.get("template_version_policy") == ALWAYS_ASK:
        #         chosen_version = CommonQuestions.ask_template_version(template.available_versions)
        #         context["template"] = template[chosen_version]
        #
        # else:
        #     context["template"] = template
        #
        # context["n_lines"] = display_template_information(context["template"])
        #
        # if len(context["template"].arguments):
        #     logger.info(Text.generate_ask_extra_parameters)
        #     context["extra_parameters"] = GenerateQuestions.ask_extra_arguments(context["template"].arguments)
        # else:
        #     context["extra_parameters"] = {}
        #
        # context["read_more_link"] = context["template"].read_more_link

        context["confirmation_response"] = GenerateQuestions.confirm_generate_all()

        return context
