import json
import gryphon.core as gryphon
from .constants import BACK, TYPING, CHILDREN, NAME
from .functions import erase_lines, get_current_tree_state_add, filter_chosen_option
from .questions import Questions


def add(data_path, _):
    """add templates based on arguments and configurations."""
    navigation_history = []

    with open(data_path / "library_tree.json") as file:
        full_tree = json.load(file)

    chosen_option = ""

    while True:
        lib_tree = get_current_tree_state_add(
            tree=full_tree,
            history=navigation_history
        )

        if not len(lib_tree):
            break

        # chosen option
        chosen_option = Questions.get_add_option(lib_tree)

        # type the bare lib name
        if chosen_option == TYPING:
            chosen_option = Questions.get_lib_via_keyboard()
            break
        elif chosen_option == BACK:
            # return to the main menu

            if len(navigation_history) >= 1:
                navigation_history.pop()
                erase_lines(n_lines=2)
            else:
                erase_lines(n_lines=2)
                return BACK
        else:
            node = filter_chosen_option(chosen_option, lib_tree)
            if CHILDREN not in node:
                chosen_option = node
                # this is the leaf item
                break
            else:
                # we are not in the leaf yet
                navigation_history.append(chosen_option)

    Questions.confirm_add(chosen_option)

    gryphon.add(
        library_name=chosen_option[NAME]
    )
