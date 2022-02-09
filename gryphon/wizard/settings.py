import json
import logging
from .functions import (
    erase_lines, get_current_tree_state,
    get_option_names, filter_chosen_option
)
from .questions import GenerateQuestions, SettingsQuestions
from ..constants import (
    BACK, YES, NO, CHILDREN, SUCCESS
)
from ..core.settings import SettingsManager


logger = logging.getLogger('gryphon')


def settings(data_path, registry):
    """Shows some configurations for power users."""

    with open(data_path / "settings_tree.json", encoding="utf-8") as file:
        full_tree = json.load(file)

    history = []
    while True:
        current_tree = get_current_tree_state(
            tree=full_tree,
            history=history
        )

        # create a list with the current possible options
        possibilities = get_option_names(current_tree)
        actual_selection = GenerateQuestions.get_generate_option(possibilities)

        if actual_selection == BACK:
            erase_lines()

            if len(history):
                history.pop()
            else:
                return BACK
            continue

        history.append(actual_selection)
        option = filter_chosen_option(actual_selection, current_tree)

        if CHILDREN not in option:
            break

    manager = SettingsManager()

    if history[0] == "Change environment manager":
        manager.change_environment_manager(actual_selection)
        logger.log(SUCCESS, f"Environment management successfully changed to {actual_selection}")

    elif history[0] == "Template repository management":
        if "Add" in history[1]:
            # ask for registry name
            registry_name = SettingsQuestions.ask_registry_name()
            if "git" in history[1]:
                # ask for git repo url
                url = SettingsQuestions.ask_git_url()
                manager.add_git_template_registry(
                    registry_name=registry_name,
                    registry_repo=url
                )

            elif "local" in history[1]:
                # ask for path
                path = SettingsQuestions.ask_local_path()
                manager.add_local_template_registry(
                    registry_name=registry_name,
                    registry_path=path
                )

        elif "Remove" in history[1]:
            registries = manager.list_template_registries()
            registry_name = SettingsQuestions.ask_which_registry_to_remove(registries)
            # ask confirmation
            manager.remove_template_registry(registry_name)

        elif "Restore" in history[1]:
            response = SettingsQuestions.confirm_restore_registry_defaults()
            if response == YES:
                manager.restore_registries()

    elif history[0] == "Restore defaults":
        response = SettingsQuestions.confirm_restore_defaults()

        if response == YES:
            manager.restore_default_config_file()
            logger.log(SUCCESS, "Factory settings restored successfully")
