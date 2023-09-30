from .generate_states import (
    AskCategory, FilterTemplates, NothingFound,
    AskTemplate, Confirmation, Install, AskKeyword,
    # Download
    ConfirmShellExec, AskProjectInfo, Download
)
from .functions import BackSignal
from ..constants import BACK
from ..fsm import Machine, HaltSignal


def generate(data_path, registry):
    """Creates a starter repository for analytics projects."""

    ask_category = AskCategory(data_path, registry)
    filter_templates = FilterTemplates()
    nothing_found = NothingFound()
    ask_template = AskTemplate()
    confirmation = Confirmation(registry)
    install = Install()
    ask_keyword = AskKeyword()
    

    possible_states = [
        ask_category, filter_templates, nothing_found,
        ask_template, confirmation, install, ask_keyword,
        ConfirmShellExec(), AskProjectInfo(), Download()
    ]

    machine = Machine(
        initial_state=ask_category,
        possible_states=possible_states
    )

    try:
        machine.run()
    except BackSignal:
        return BACK
    except HaltSignal:
        return
