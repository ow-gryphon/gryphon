import logging
import os
import json
import platform
from wizard.functions import erase_lines, get_current_tree_state, filter_chosen_option, current_folder_has_venv
from wizard.questions import AddQuestions
from wizard.wizard_text import Text
from core import add as core_add
from constants import BACK, TYPING, CHILDREN, NAME, YES, NO

logger = logging.getLogger('gryphon')


def add(data_path, _):
    """add templates based on arguments and configurations."""

    if not current_folder_has_venv():
        logger.warning(Text.no_virtual_environment_remainder)

    navigation_history = []
    chosen_option = ""

    with open(data_path / "library_tree.json", encoding='utf-8') as file:
        full_tree = json.load(file)

    while True:
        lib_tree = get_current_tree_state(
            tree=full_tree,
            history=navigation_history
        )

        if not len(lib_tree):
            break

        # chosen option
        chosen_option = AddQuestions.get_add_option(lib_tree)

        if chosen_option == BACK:
            # return to the main menu
            if len(navigation_history) >= 1:
                navigation_history.pop()
                erase_lines(n_lines=2)
                continue
            else:
                erase_lines(n_lines=2)
                return BACK
        elif chosen_option == TYPING:
            # type the bare lib name
            chosen_option = {NAME: AddQuestions.get_lib_via_keyboard()}
        else:
            node = filter_chosen_option(chosen_option, lib_tree)
            if CHILDREN not in node:
                # this is the leaf item
                chosen_option = node
            else:
                # we are not in the leaf yet
                navigation_history.append(chosen_option)
                continue

        response = None
        while response != YES:

            response, n_lines = AddQuestions.confirm_add(chosen_option)

            if response == NO:
                # navigation_history.pop()
                erase_lines(n_lines=2)
                erase_lines(n_lines=n_lines)
                break

            if response != YES:

                if platform.system() == "Windows":
                    os.system(f"start {response}")
                    erase_lines(n_lines=1)
                else:
                    os.system(f"""nohup xdg-open "{response}" """)
                    os.system(f"""rm nohup.out""")
                    erase_lines()
                erase_lines(n_lines=n_lines)

        if response == NO:
            continue

        break

    core_add(
        library_name=chosen_option[NAME]
    )