"""
File containing the CommandLoader class that is used to load
the templates metadata into memory.
"""

import os
import logging
import sys
from pathlib import Path
import json
import glob
from .template import Template


logger = logging.getLogger('gryphon')


def insert_index_name(metadata, index_type):
    metadata["display_name"] = f'{metadata["display_name"]} ({index_type})'
    return metadata


class TemplateRegistry:
    """Class that loads commands and metadata from the ./data folder."""
    type = ""

    def __init__(self, templates_path: Path):
        self.path = templates_path

        self.template_data = {}

        for command_name in ['add', 'generate', 'init']:
            glob_pattern = self.path / command_name / "*"
            folders = glob.glob(str(glob_pattern))

            if len(folders) == 0:
                self.template_data[command_name] = {}
                continue

            self.template_data[command_name] = {
                f"{os.path.basename(path)}_{self.type}": Template(
                    template_name=os.path.basename(path),
                    template_path=Path(path),
                    template_metadata=self.load_metadata(Path(path)),
                    registry_type=self.type
                )
                for path in folders
            }

    def get_templates(self, command=None):
        """Returns the template metadata."""
        if command is None:
            return self.template_data

        assert command in ['add', 'generate', 'init']
        return self.template_data[command]

    def update_registry(self):
        raise NotImplementedError

    @staticmethod
    def load_metadata(path: Path):
        """Loads the metadata file inside template folder."""
        try:
            filename = path / "metadata.json"
            with open(filename, encoding='UTF-8') as file:
                return json.load(file)
        except FileNotFoundError:
            if 'pytest' in sys.modules:
                print(f"template at {path} does not contain a metadata.json file.")
            logger.warning(f"template at {path} does not contain a metadata.json file.")
            return {}
        except json.JSONDecodeError:
            if 'pytest' in sys.modules:
                print(f"template at {path} has a malformed json on metadata.json file.")
            logger.warning(f"template at {path} has a malformed json on metadata.json file.")
            return {}
