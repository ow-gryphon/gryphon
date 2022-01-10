import json
import gryphon.core as gryphon
from .constants import NODE, BACK, TYPING, LEAF_OPTIONS
from .functions import erase_lines, get_current_tree_state
from .questions import Questions


def add(data_path, _):
    """add templates based on arguments and configurations."""
    level = 0
    navigation_history = []

    with open(data_path / "library_category_tree.json") as file:
        full_tree = json.load(file)

    while True:
        lib_tree = get_current_tree_state(
            tree=full_tree,
            history=navigation_history
        )

        # create a list with the current possible options

        possibilities = list(lib_tree.keys())
        possibilities.extend(lib_tree[LEAF_OPTIONS])
        possibilities.remove(LEAF_OPTIONS)

        # chosen option
        chosen_option = Questions.get_add_option(possibilities)

        # type the bare lib name
        if chosen_option == TYPING:
            chosen_option = Questions.get_lib_via_keyboard()
            break
        elif chosen_option == BACK:
            # return to the main menu

            if len(navigation_history) >= 1:
                navigation_history.pop()
                erase_lines(n_lines=2)
                level -= 1
                continue
            else:
                erase_lines(n_lines=2)
                return BACK

        elif chosen_option in lib_tree[LEAF_OPTIONS]:
            # this is the leaf item
            break
        else:
            # we are not in the leaf yet
            level += 1
            navigation_history.append(chosen_option)

    Questions.confirm_add(chosen_option)

    gryphon.add(
        library_name=chosen_option
    )
