import json
from pathlib import Path
from typing import Dict, List

from .operations import RCManager, NBStripOutManager, NBExtensionsManager, PreCommitManager
from ..constants import NB_EXTENSIONS, NB_STRIP_OUT, PRE_COMMIT_HOOKS, SUCCESS
from ..logger import logger


def get_addon_states(rc_file: Path):

    assert rc_file.is_file()

    with open(rc_file, "r", encoding="utf-8") as f:
        contents = json.load(f)

        return {
            NB_EXTENSIONS: contents[NB_EXTENSIONS] if NB_EXTENSIONS in contents else False,
            NB_STRIP_OUT: contents[NB_STRIP_OUT] if NB_STRIP_OUT in contents else False,
            PRE_COMMIT_HOOKS: contents[PRE_COMMIT_HOOKS] if PRE_COMMIT_HOOKS in contents else False,
        }


def set_new_addon_states(new_states: Dict[str, bool], rc_file: Path):
    RCManager.set_addon_states(
        install_nb_strip_out=new_states[NB_STRIP_OUT],
        install_nbextensions=new_states[NB_EXTENSIONS],
        install_pre_commit_hooks=new_states[PRE_COMMIT_HOOKS],
        logfile=rc_file
    )


def sync_addons_with_state(state: Dict[str, bool], changes: List[str], rc_file: Path):

    env_path = RCManager.get_environment_manager_path(rc_file)
    env_manager = RCManager.get_environment_manager(rc_file)

    if NB_STRIP_OUT in changes:
        if state[NB_STRIP_OUT]:
            # activate
            NBStripOutManager.setup(rc_file.parent, env_path)
        else:
            # deactivate
            NBStripOutManager.teardown(rc_file.parent, env_path)

    if NB_EXTENSIONS in changes:
        if state[NB_EXTENSIONS]:
            # activate
            NBExtensionsManager.install(environment_manager=env_manager, environment_path=env_path)
        else:
            # deactivate
            NBExtensionsManager.teardown(environment_manager=env_manager, environment_path=env_path)

    if PRE_COMMIT_HOOKS in changes:
        if state[PRE_COMMIT_HOOKS]:
            # activate
            PreCommitManager.full_setup(location=rc_file.parent, environment_path=env_path)
        else:
            # deactivate
            PreCommitManager.teardown(location=rc_file.parent, environment_path=env_path)

    return state


def configure_project(new_activated_addons: List[str], logfile: Path):
    current_addons = get_addon_states(logfile)

    new_addons = {
        NB_EXTENSIONS: NB_EXTENSIONS in new_activated_addons,
        NB_STRIP_OUT: NB_STRIP_OUT in new_activated_addons,
        PRE_COMMIT_HOOKS: PRE_COMMIT_HOOKS in new_activated_addons,
    }

    changed = [
        k
        for k in new_addons.keys()
        if new_addons[k] != current_addons[k]
    ]

    sync_addons_with_state(
        state=new_addons,
        changes=changed,
        rc_file=logfile
    )

    set_new_addon_states(new_addons, rc_file=logfile)

    logger.log(SUCCESS, "Successfully updated project addons.")
