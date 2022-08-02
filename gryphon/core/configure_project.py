import json
from pathlib import Path
from typing import Dict

from .operations import RCManager
from ..constants import NB_EXTENSIONS, NB_STRIP_OUT, PRE_COMMIT_HOOKS


def get_addon_states(rc_file: Path):

    assert rc_file.is_file()

    with open(rc_file, "r", encoding="utf-8") as f:
        contents = json.load(f)

        return {
            NB_EXTENSIONS: contents[NB_EXTENSIONS] if NB_EXTENSIONS in contents else False,
            NB_STRIP_OUT: contents[NB_STRIP_OUT] if NB_STRIP_OUT in contents else False,
            PRE_COMMIT_HOOKS: contents[PRE_COMMIT_HOOKS] if PRE_COMMIT_HOOKS in contents else False,
        }


def set_new_addon_states(new_states: Dict[str, bool]):
    RCManager.set_addon_states(
        install_nb_strip_out=new_states[NB_STRIP_OUT],
        install_nbextensions=new_states[NB_EXTENSIONS],
        install_pre_commit_hooks=new_states[PRE_COMMIT_HOOKS]
    )


def sync_addons_with_state(state: Dict[str, bool]):
    # TODO: CREATE METHODS TO UNINSTALL EACH OF THE ADDONS
    return state
