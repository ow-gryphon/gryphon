import logging

from ..questions import DownloadQuestions
from ...constants import YES, NO, SUCCESS
from ...fsm import State, Transition

logger = logging.getLogger('gryphon')


def _change_from_exec_confirmation_to_ask_project_info(context: dict) -> bool:
    confirmed = context["confirmed"]
    
    if confirmed == NO:
        logger.log(SUCCESS, "Note: Manual installation may be required following the download of this repository.") 
    
    return confirmed == YES or confirmed == NO


class ConfirmShellExec(State):

    name = "confirm_shell_exec"

    transitions = [
        Transition(
            next_state="ask_project_info",
            condition=_change_from_exec_confirmation_to_ask_project_info
        )
    ]

    def on_start(self, context: dict) -> dict:
        template = context["template"]

        context["n_lines_warning"] = 0

        confirmed, n_lines = DownloadQuestions.confirm_shell_execution(
            template=template
        )

        context.update(dict(
            n_lines=n_lines,
            confirmed=confirmed
        ))
        context["extra_parameters"]["confirm_shell_exec"] = context["confirmed"] == YES

        return context
