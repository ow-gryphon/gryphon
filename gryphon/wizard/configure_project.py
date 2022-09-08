from pathlib import Path

from .functions import erase_lines
from .questions import ConfigureProjectQuestions
from ..constants import GRYPHON_RC, BACK
from ..core.configure_project import get_addon_states, configure_project as core_configure_project


def configure_project(_, __):
    logfile = Path.cwd() / GRYPHON_RC
    current_addons = get_addon_states(logfile)

    new_activated_addons = ConfigureProjectQuestions.ask_addons(current_addons)

    if new_activated_addons == BACK:
        erase_lines(2)
        return BACK

    core_configure_project(new_activated_addons, logfile)
