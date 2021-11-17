import os
from os import path
from labskit_commands.command_operations import copy_project_template
import utils


def test_copy_project_template():
    """
    Tests if the template folder is being properly copied.
    """
    destination_folder = "trivial_template"
    copy_project_template(
        command="init",
        template="trivial",
        folder=destination_folder
    )
    absolute_folder_path = path.join(os.getcwd(), destination_folder)

    try:
        assert path.isdir(absolute_folder_path)
        assert path.isfile(f"{absolute_folder_path}/requirements.txt")
        assert path.isfile(f"{absolute_folder_path}/sample_template")

    finally:
        utils.remove_folder(absolute_folder_path)
