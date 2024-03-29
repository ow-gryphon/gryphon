import os
import logging
import platform
from pathlib import Path
from typing import Tuple
from textwrap import fill
from ..constants import (
    CHILDREN, NAME, VENV_FOLDER, VALUE, DATA_PATH, ERASE_LINE
)


logger = logging.getLogger('gryphon')


class BackSignal(Exception):
    def __init__(self):
        super().__init__()


def erase_lines(n_lines=2):
    for _ in range(n_lines):
        logger.info(ERASE_LINE)


def wrap_text(text) -> Tuple[str, int]:
    wrapped = ""
    for i in text.split('\n'):
        line = fill(
            i, width=100, drop_whitespace=False,
            expand_tabs=True, replace_whitespace=False,
            break_on_hyphens=True, subsequent_indent='\t'
        )
        wrapped += '\n' + line

    n_lines = len(wrapped.split('\n'))

    return wrapped, n_lines


def display_template_information(template) -> int:
    information = ""

    information += f'\t{template.display_name}\n\n\t{template.description}\n\n'

    if len(template.topic):
        information += f"\tTopics: {', '.join(template.topic)}\n"

    if len(template.sector):
        information += f"\tSectors: {', '.join(template.sector)}\n"

    if len(template.methodology):
        information += f"\tMethodology: {', '.join(template.methodology)}\n"

    wrapped, n_lines = wrap_text(information)
    logger.info(wrapped)

    if template.approver:
        approver_warning_text = f"\tNOTE: This template requires author approval. " \
                                f"Please contact {template.approver} for access to the repository before attempting " \
                                f"to use this template. If you do not yet have MMC GitHub access, please see the " \
                                f"link below to get set up.\n"
        wrapped, n_lines_approver = wrap_text(approver_warning_text)
        logger.error(wrapped)
        n_lines += n_lines_approver

    return n_lines


def get_current_tree_state(tree, history):
    if not len(history):
        return tree

    tree_level = tree.copy()

    for item in history:
        tree_level = filter_chosen_option(item, tree_level).get(CHILDREN, [])

    return tree_level


def get_current_tree_state_by_value(tree, history):
    if not len(history):
        return tree

    tree_level = tree.copy()

    for item in history:
        tree_level = filter_chosen_option_by_value(item, tree_level).get(CHILDREN, [])

    return tree_level


def filter_chosen_option(option, tree):
    try:
        return list(filter(lambda x: x[NAME] == option, tree))[0]
    except IndexError:
        raise ValueError("Error in the menu navigation (name search).")


def filter_chosen_option_by_value(option, tree):
    try:
        return list(filter(lambda x: x[VALUE] == option, tree))[0]
    except IndexError:
        raise ValueError("Error in the menu navigation (value search).")


def get_option_names(tree):
    return list(map(lambda x: x[NAME], tree))


def current_folder_has_venv():
    cwd = Path.cwd()
    if platform.system() == "Windows":
        activate_path = cwd / VENV_FOLDER / "Scripts" / "activate.bat"
    else:
        activate_path = cwd / VENV_FOLDER / "bin" / "activate"

    return activate_path.is_file()


def list_conda_available_python_versions():
    logger.info("Listing possible python versions ...")
    logger.info("It might take a while ...")

    version_file = DATA_PATH / "versions_raw.txt"
    os.system(f'conda search python -k >> \"{version_file}\"')
    with open(version_file, "r", encoding="UTF-8") as f:
        line = True
        all_versions = []
        while line:
            line = f.readline()
            if "python" in line:
                version = line[6:].strip().split(' ')[0]
                all_versions.append(version)

    displayed_versions = set(
        map(
            lambda x: '.'.join(x.split(".")[:-1]),
            all_versions
        )
    )
    erase_lines()

    displayed_versions = sorted(
        displayed_versions,
        key=lambda x: int(x.split(".")[1]) if "." in x else 0
    )

    displayed_versions = sorted(
        displayed_versions,
        key=lambda x: x.split(".")[0]
    )

    # no version lower than 3.7 will be permitted
    major = 3
    minor = 7
    possible_versions = list(filter(
        lambda x: x.split(".")[0] >= str(major) and int(x.split(".")[1]) >= minor,
        displayed_versions
    ))
    return possible_versions
