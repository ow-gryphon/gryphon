"""
File containing the CommandLoader class that is used to load
the templates metadata into memory.
"""

import os
import sys
import json
import logging
import glob
from pathlib import Path
from typing import List
from .template import Template
from ...constants import INIT, GENERATE, DOWNLOAD


logger = logging.getLogger('gryphon')


def insert_index_name(metadata, index_type):
    metadata["display_name"] = f'{metadata["display_name"]} ({index_type})'
    return metadata


class TemplateRegistry:
    """Class that loads commands and metadata from the ./data folder."""
    type = ""

    def __init__(self, templates_root: Path = None, template_paths: List[Path] = None):
        self.template_data = {
            INIT: {},
            GENERATE: {},
            DOWNLOAD: {},
        }

        if template_paths is not None:
            folders = template_paths

        elif templates_root is not None:
            self.path = templates_root
            glob_pattern = self.path / "*"
            folders = glob.glob(str(glob_pattern))

        else:
            raise RuntimeError("One of [\"templates_root\", \"template_paths\"] arguments must be passed.")

        if len(folders) == 0:
            return

        for path in folders:
            try:
                metadata = self.load_metadata(Path(path))
            except FileNotFoundError:
                logger.warning(f"Could not find template at location: {path}")
                continue
            if "command" not in metadata:
                continue

            command = metadata["command"]
            if command not in ['add', 'generate', 'init', 'download']:
                continue

            name = os.path.basename(path)

            self.template_data[command].update({
                f"{name}_{self.type}": Template(
                    template_name=name,
                    template_path=Path(path),
                    template_metadata=metadata,
                    registry_type=self.type
                )
            })

    def get_templates(self, command=None):
        """Returns the template metadata."""
        if command is None:
            return self.template_data

        assert command in ['add', 'generate', 'init', 'download']
        return self.template_data[command]

    def update_registry(self):
        raise NotImplementedError

    @staticmethod
    def load_metadata(path: Path):
        """Loads the metadata file inside template folder."""
        if not path.is_dir():
            raise FileNotFoundError(f"Template folder does not exist (anymore): {path}")

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
