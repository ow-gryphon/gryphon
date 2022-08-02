from pathlib import Path

from .functions import erase_lines
from .questions import ConfigureProjectQuestions
from ..constants import GRYPHON_RC, NB_EXTENSIONS, NB_STRIP_OUT, PRE_COMMIT_HOOKS, BACK, SUCCESS
from ..core.configure_project import get_addon_states, set_new_addon_states, sync_addons_with_state
from ..logger import logger


def configure_project(_, __):

    current_addons = get_addon_states(Path.cwd() / GRYPHON_RC)
    new_activated_addons = ConfigureProjectQuestions.ask_addons(current_addons)

    if new_activated_addons == BACK:
        erase_lines(2)
        return BACK

    new_addons = {
        NB_EXTENSIONS: NB_EXTENSIONS in new_activated_addons,
        NB_STRIP_OUT: NB_STRIP_OUT in new_activated_addons,
        PRE_COMMIT_HOOKS: PRE_COMMIT_HOOKS in new_activated_addons,
    }

    set_new_addon_states(new_addons)

    sync_addons_with_state(new_addons)
    logger.log(SUCCESS, "Successfully updated project addons.")
