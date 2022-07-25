import json
import os
import platform
from pathlib import Path
from typing import List

from gryphon.constants import DATA_PATH, NAME, CHILDREN
from .constants import KEY_DOWN, KEY_UP, WELCOME_MESSAGE, SUCCESS_MESSAGE
from .constants import SELECT_TEMPLATE, NAVIGATE_CATEGORIES, CONFIRMATION_MESSAGE

if platform.system() != "Windows":
    import pexpect
else:
    # noinspection PyUnresolvedReferences
    import wexpect as pexpect


def start_wizard(working_directory: Path) -> pexpect.spawn:
    os.chdir(working_directory)
    process = pexpect.spawn(
        command=f'gryphon -d',
        encoding='utf-8',
        maxread=4000
    )
    wait_for_output(process, WELCOME_MESSAGE)
    return process


def quit_process(process):
    process.close()


def enter(process):
    process.sendcontrol('m')


def key_down(process, times=1):
    for _ in range(times):
        process.send(KEY_DOWN)


def key_up(process, times=1):
    for _ in range(times):
        process.send(KEY_UP)


def type_text(process, text: str):
    process.send(text)


def wait_for_output(process, text: str, timeout=10):
    process.expect(text, timeout=timeout)
    print(f"Found \"{text}\" on the outputs.")


def select_nth_option(process, n: int):
    assert n >= 1
    key_down(process, times=n-1)
    enter(process)


def wait_for_success(process):
    wait_for_output(process, SUCCESS_MESSAGE, timeout=180)


def navigate_categories(process, categories: List[str]):
    lib_tree_path = Path(DATA_PATH) / "category_tree.json"

    with open(lib_tree_path, "r", encoding="UTF-8") as f:
        lib_tree = json.load(f)

    level = 0
    idx = 0
    actual_level = lib_tree.copy()
    while 1:

        node = actual_level[idx]
        name = node[NAME]
        print(name)
        if name == categories[level]:
            select_nth_option(process, idx + 1)
            if CHILDREN not in node:
                break

            wait_for_output(process, NAVIGATE_CATEGORIES, timeout=10)
            actual_level = node[CHILDREN]

            level += 1
            idx = 0
        else:
            idx += 1

    wait_for_output(process, SELECT_TEMPLATE, timeout=10)


def navigate_libraries(process, categories: List[str]):
    lib_tree_path = Path(DATA_PATH) / "library_tree.json"

    with open(lib_tree_path, "r", encoding="UTF-8") as f:
        lib_tree = json.load(f)

    level = 0
    idx = 0
    actual_level = lib_tree.copy()
    while 1:

        node = actual_level[idx]
        name = node[NAME]
        print(name)
        if name == categories[level]:
            select_nth_option(process, idx + 1)
            if CHILDREN not in node:
                break

            wait_for_output(process, NAVIGATE_CATEGORIES, timeout=10)
            actual_level = node[CHILDREN]

            level += 1
            idx = 0
        else:
            idx += 1


def confirm_information(process):
    wait_for_output(process, CONFIRMATION_MESSAGE)
    enter(process)
