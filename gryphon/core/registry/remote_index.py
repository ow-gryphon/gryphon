import os
import json
import glob
from typing import List, Dict
from pathlib import Path
from git import Repo
from distutils.version import StrictVersion
from .template import Template
from ..common_operations import remove_folder
from ...constants import GRYPHON_HOME


class RemoteIndex:
    def __init__(self, index_url: str, index_repo: str, index_name: str):
        self.index_url = index_url
        self.index_repo = index_repo
        self.index_local_path = GRYPHON_HOME / "index" / index_name

        if not self.index_local_path.is_dir():
            os.makedirs(self.index_local_path)
        else:
            remove_folder(self.index_local_path)

        self.repo = Repo.clone_from(self.index_repo, self.index_local_path)

        self.metadata = self.read_index_metadata()
        self.templates = self.generate_templates()

    def read_index_metadata(self) -> Dict[str, List]:
        metadata_files = glob.glob(str(self.index_local_path / "**" / "metadata.json"), recursive=True)
        metadata_contents = {
            "generate": [],
            "init": []
        }
        for file in metadata_files:
            with open(file, "r", encoding="UTF-8") as f:
                contents = json.load(f)

                versions = list(contents.keys())
                versions.sort(key=lambda x: StrictVersion(x[1:]))

                latest_version = list(contents.keys())[-1]
                latest = contents[latest_version]

                latest["path"] = Path(file).parent
                command = latest["command"]
                assert command in ["generate", "init"]
                metadata_contents[command].append(latest)

        return metadata_contents

    def generate_templates(self) -> Dict[str, Dict[str, Template]]:
        templates = {
            "generate": {},
            "init": {}
        }
        for command, metadata_list in self.metadata.items():
            templates[command].update({
                metadata["path"].parts[-1]: Template(
                    template_name=metadata["path"].parts[-1],
                    template_path=self.index_url,
                    template_metadata=metadata,
                    registry_type="remote index"
                )
                for metadata in metadata_list
            })

        return templates

    def get_templates(self, command=None):
        """Returns the template metadata."""
        if command is None:
            return self.templates

        assert command in ['add', 'generate', 'init']
        return self.templates[command]


class TemplateCollection:
    def __init__(self, index_list: List[Dict[str, str]]):
        self.index_list = index_list

        self.indexes = self.create_indexes()
        self.templates = self.unify_templates()

    def create_indexes(self) -> List[RemoteIndex]:
        return [
            RemoteIndex(index_url=links["url"], index_repo=links["repo"], index_name=links["name"])
            for links in self.index_list
        ]

    def unify_templates(self) -> Dict[str, Dict[str, Template]]:
        templates = {
            "generate": {},
            "init": {}
        }
        for index in self.indexes:
            for command, temp in index.get_templates().items():
                templates[command].update(temp)
        return templates

    def get_templates(self, command=None):
        """Returns the template metadata."""
        if command is None:
            return self.templates

        assert command in ['add', 'generate', 'init']
        return self.templates[command]
