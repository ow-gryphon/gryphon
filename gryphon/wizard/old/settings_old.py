import json
import logging
from .functions import (
    erase_lines, get_current_tree_state_by_value,
    filter_chosen_option_by_value, list_conda_available_python_versions
)
from .questions import SettingsQuestions, InitQuestions
from ..core.common_operations import get_current_python_version
from ..constants import (
    BACK, YES, CHILDREN, SUCCESS, CONFIG_FILE, DEFAULT_ENV,
    NAME, VALUE, ALWAYS_ASK
)
from ..core.settings import SettingsManager


logger = logging.getLogger('gryphon')


def back_to_previous(history, **kwargs):
    history.pop()
    erase_lines(**kwargs)


def handle_current_env_manager(tree_level):
    with open(CONFIG_FILE, "r", encoding="UTF-8") as f:
        current_env = json.load(f).get("environment_management", DEFAULT_ENV)

    response = []
    for p in tree_level:
        p = p.copy()
        name = p.pop(NAME)
        entry = dict(
            name=f"{name} (current)" if p[VALUE].lower() == current_env else name,
            **p
        )
        response.append(entry)
    return response


def settings(data_path, _):
    """Shows some configurations for power users."""

    with open(data_path / "settings_tree.json", encoding="utf-8") as file:
        full_tree = json.load(file)

    history = []
    while True:
        current_tree = get_current_tree_state_by_value(
            tree=full_tree,
            history=history
        )

        if len(history) and history[0] == "change_env_manager":
            current_tree = handle_current_env_manager(current_tree)

        actual_selection = SettingsQuestions.get_option(current_tree)

        if actual_selection == BACK:
            erase_lines()

            if len(history):
                history.pop()
            else:
                return BACK
            continue

        history.append(actual_selection)
        option = filter_chosen_option_by_value(actual_selection, current_tree)

        if CHILDREN in option:
            continue

        manager = SettingsManager()
        if history[0] == "change_python_version":

            versions = list_conda_available_python_versions()
            selected_option = SettingsQuestions.ask_python_version(versions, get_current_python_version())

            if selected_option == BACK:
                back_to_previous(history, n_lines=2)
                continue
            else:
                manager.change_default_python_version(selected_option)
                if selected_option == ALWAYS_ASK:
                    logger.log(SUCCESS, f"The python version will be asked for every new project.")
                else:
                    logger.log(SUCCESS, f"Default python version set to {selected_option}")

        elif history[0] == "new_template":
            # ask for the folder
            location = InitQuestions.ask_just_location()

            manager.render_template_scaffolding(location)

        elif history[0] == "change_env_manager":
            response = SettingsQuestions.confirm_change_env_manager(actual_selection)
            if response == YES:
                manager.change_environment_manager(actual_selection.lower())
                logger.log(SUCCESS, f"Environment management successfully changed to {actual_selection}")
            else:
                back_to_previous(history, n_lines=3)
                continue

        elif history[0] == "registry_options":
            if "add" in history[1]:
                # ask for registry name
                registry_name = SettingsQuestions.ask_registry_name()
                if "remote" in history[1]:
                    # ask for git repo url
                    url = SettingsQuestions.ask_git_url()
                    response = SettingsQuestions.confirm_registry_addition(registry_name)
                    if response == YES:
                        manager.add_git_template_registry(
                            registry_name=registry_name,
                            registry_repo=url
                        )
                        logger.log(SUCCESS, f"Successfully added registry {registry_name}.")
                    else:
                        back_to_previous(history, n_lines=4)
                        continue

                elif "local" in history[1]:
                    # ask for path
                    path = SettingsQuestions.ask_local_path()
                    response = SettingsQuestions.confirm_registry_addition(registry_name)
                    if response == YES:
                        manager.add_local_template_registry(
                            registry_name=registry_name,
                            registry_path=path
                        )
                        logger.log(SUCCESS, f"Successfully added registry {registry_name}.")
                    else:
                        back_to_previous(history, n_lines=4)
                        continue

            elif history[1] == "remove_registry":
                registries = manager.list_template_registries()
                registry_name = SettingsQuestions.ask_which_registry_to_remove(registries)
                # ask for confirmation
                if registry_name == BACK:
                    back_to_previous(history)
                    continue

                result = SettingsQuestions.confirm_remove_registry()
                if result == YES:
                    manager.remove_template_registry(registry_name)
                    logger.log(SUCCESS, f"Successfully removed registry {registry_name}.")
                else:
                    back_to_previous(history, n_lines=3)
                    continue

            elif "restore_default_registry" in history[1]:
                response = SettingsQuestions.confirm_restore_registry_defaults()
                if response == YES:
                    manager.restore_registries()
                    logger.log(SUCCESS, f"Successfully restored registry to defaults.")
                else:
                    back_to_previous(history, n_lines=3)
                    continue

        elif history[0] == "restore_defaults":
            response = SettingsQuestions.confirm_restore_defaults()

            if response == YES:
                manager.restore_default_config_file()
                logger.log(SUCCESS, "Factory settings restored successfully")
            else:
                back_to_previous(history, n_lines=3)
                continue

        history = []
        print("\n")
