"""
File containing the CommandLoader class that is used to load
the templates metadata into memory.
"""

import os
import json
import glob
from labskit_commands.logging import Logging


class TemplateRegistry:
    """Class that loads commands and metadata from the ./data folder."""

    def __init__(self, templates_path):
        self.path = templates_path

        self.template_data = {}

        for command_name in ['add', 'generate', 'init']:
            glob_pattern = os.path.join(self.path, command_name, "*")
            folders = glob.glob(glob_pattern)

            if len(folders) == 0:
                self.template_data[command_name] = {}
                continue

            self.template_data[command_name] = {
                os.path.basename(path): {
                        "path": path,
                        "metadata": self.load_metadata(path)
                    }
                for path in folders
            }

    def get_metadata(self):
        """Returns the template metadata."""
        return self.template_data

    def update_registry(self):
        raise NotImplementedError

    @staticmethod
    def load_metadata(path):
        """Loads the metadata file inside template folder."""
        try:
            filename = os.path.join(path, "metadata.json")
            with open(filename, encoding='UTF-8') as file:
                return json.load(file)
        except FileNotFoundError:
            Logging.warn(f"template at {path} does not contain a metadata.json file.")
            return {}
        except json.JSONDecodeError:
            Logging.warn(f"template at {path} has a malformed json on metadata.json file.")
            return {}
