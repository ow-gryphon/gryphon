import json
import gryphon.core as gryphon
from .constants import *
from .functions import *
from .questions import Questions


def get_current_tree_state(tree, history):
    tree_level = tree.copy()

    for item in history:
        if item in tree_level:
            tree_level = tree_level[item]
            return tree_level
        elif item in tree_level['leaf_options']:
            return {}
        else:
            raise RuntimeError("Error in tree navigation.")


def add(data_path, _):
    """add templates based on arguments and configurations."""
    while True:
        with open(data_path / "library_category_tree.json") as file:
            lib_tree = json.load(file)

        level = -1
        # loop to return to the category prompt
        while True:
            # TODO: REMOVE this loop and use a predefined menu structure
            level += 1
            possibilities = list(lib_tree.keys())
            possibilities.remove("leaf_options")

            choices = {
                option: "node"
                for option in possibilities
            }

            choices.update({
                option: "leaf"
                for option in lib_tree["leaf_options"]
            })

            # categories
            library_name = Questions.get_add_option(list(choices.keys()))

            # type the bare lib name
            if library_name == "type":
                library_name = Questions.get_lib_via_keyboard()
                break
            elif library_name == BACK:
                # return to the main menu
                if level > 0:
                    erase_lines(n_lines=level + 1)
                    break
                else:
                    erase_lines(n_lines=level + 2)
                    return BACK
            elif choices[library_name] == "node":
                lib_tree = lib_tree[library_name]
            else:
                break

        if library_name == BACK and level > 0:
            continue

        Questions.confirm_add(library_name)

        gryphon.add(
            library_name=library_name
        )
        break
