from .generate_all_templates_states import Confirmation, Install
from .functions import BackSignal
from ..constants import BACK
from ..fsm import Machine, HaltSignal


def generate_all_templates(data_path, registry):
    """Download all methodology templates into the current gryphon project"""

#    ask_category = AskCategory(data_path, registry)
#    filter_templates = FilterTemplates()
#    nothing_found = NothingFound()
#    ask_template = AskTemplate()
    confirmation = Confirmation(registry)
    install = Install()
#    ask_keyword = AskKeyword()

    possible_states = [
        confirmation, install
    ]

    machine = Machine(
        initial_state=confirmation,
        possible_states=possible_states
    )

    try:
        machine.run()
    except BackSignal:
        return BACK
    except HaltSignal:
        return
