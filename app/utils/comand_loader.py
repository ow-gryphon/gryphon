"""
File containing the CommandLoader class that is used to load
the templates metadata into memory.
"""

import os
import json
import glob
import click


TEMPLATES_FOLDER = os.path.join(os.getcwd(), "data")


class CommandLoader:
    """Class that loads commands and metadata from the ./data folder."""

    def __init__(self, command_name, package_path=None):
        self.command = command_name
        if package_path is not None:
            path = package_path
        else:
            path = TEMPLATES_FOLDER

        self._folders = glob.glob(f"{path}/{command_name}/*")

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
        return path.split("/")[-1]

    @staticmethod
    def load_metadata(path):
        """Loads the metadata file inside template folder."""
        try:
            with open(f"{path}/metadata.json", encoding='UTF-8') as file:
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
