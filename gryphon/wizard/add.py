import json
import gryphon.core as gryphon
from .constants import NODE, LEAF, BACK, TYPING, LEAF_OPTIONS
from .functions import erase_lines
from .questions import Questions


def get_current_tree_state(tree, history):
    tree_level = tree.copy()

    for item in history:
        if item in tree_level:
            tree_level = tree_level[item]
        else:
            raise RuntimeError("Error in tree navigation.")

    return tree_level


def add(data_path, _):
    """add templates based on arguments and configurations."""
    level = -1
    navigation_history = []

    with open(data_path / "library_category_tree.json") as file:
        full_tree = json.load(file)

    while True:
        lib_tree = get_current_tree_state(
            tree=full_tree,
            history=navigation_history
        )

        possibilities = list(lib_tree.keys())
        possibilities.append(lib_tree[LEAF_OPTIONS])
        possibilities.remove(LEAF_OPTIONS)

        choices = {
            option: NODE
            for option in possibilities
        }

        choices.update({
            option: LEAF
            for option in lib_tree[LEAF_OPTIONS]
        })

        # chosen option
        level += 1
        chosen_option = Questions.get_add_option(list(choices.keys()))

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
                erase_lines(n_lines=level)
                return BACK
        elif choices[chosen_option] == NODE:
            navigation_history.append(chosen_option)
        elif choices[chosen_option] == LEAF:
            # this is the leaf item
            break

    Questions.confirm_add(chosen_option)

    gryphon.add(
        library_name=chosen_option
    )
