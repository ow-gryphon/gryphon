"""
File containing the CommandLoader class that is used to load
the templates metadata into memory.
"""

import os
import json
import glob
import click


TEMPLATES_FOLDER = os.path.abspath("data")
PACKAGE_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = os.path.join(PACKAGE_PATH, "labskit_commands", "data")


class CommandLoader:
    """Class that loads commands and metadata from the ./data folder."""

    def __init__(self, command_name, templates_path=None):
        self.command = command_name
        if templates_path is not None:
            path = templates_path
        else:
            path = TEMPLATES_FOLDER

        glob_pattern = os.path.join(path, command_name, "*")
        self._folders = glob.glob(glob_pattern)

        if len(self._folders) == 0:
            self.template_data = {}
            return

        self.template_data = {
            self.get_leaf_folder_name(path): {
                    "path": path,
                    "metadata": self.load_metadata(path)
                }
            for path in self._folders
        }

    def get_metadata(self):
        """Returns the template metadata."""
        return self.template_data

    @staticmethod
    def get_leaf_folder_name(path):
        """Gets the name of the leaf node."""
        return os.path.basename(path)

    @staticmethod
    def load_metadata(path):
        """Loads the metadata file inside template folder."""
        try:
            filename = os.path.join(path, "metadata.json")
            with open(filename, encoding='UTF-8') as file:
                return json.load(file)
        except FileNotFoundError:
            click.secho(
                f"WARNING template at {path} does not contain a metadata.json file.",
                fg='yellow'
            )
            return {}
        except json.JSONDecodeError:
            click.secho(
                f"WARNING template at {path} has a malformed json on metadata.json file.",
                fg='yellow'
            )
            return {}
