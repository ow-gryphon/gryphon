import os
import json
import glob
from typing import List, Dict
from pathlib import Path
from git import Repo
from .template import Template
from .versioned_template import VersionedTemplate
from ..common_operations import remove_folder, sort_versions
from ...constants import GRYPHON_HOME, GENERATE, INIT, REMOTE_INDEX


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
            GENERATE: [],
            INIT: []
        }
        for file in metadata_files:
            with open(file, "r", encoding="UTF-8") as f:
                contents = json.load(f)
                versions = list(contents.keys())

                latest_version = sort_versions(versions)[-1]
                latest = contents[latest_version]

                contents["path"] = Path(file).parent

                command = latest["command"]
                assert command in [GENERATE, INIT]
                metadata_contents[command].append(contents)

        return metadata_contents

    def generate_templates(self) -> Dict[str, Dict[str, Template]]:
        templates = {
            GENERATE: {},
            INIT: {}
        }

        for command, metadata_list in self.metadata.items():
            for metadata in metadata_list:
                path = metadata.pop("path")
                templates[command].update({
                    path.parts[-1]: VersionedTemplate(
                        template_name=path.parts[-1],
                        template_path=self.index_url,
                        template_metadata=metadata,
                        registry_type=REMOTE_INDEX
                    )
                    for metadata in metadata_list
                })

        return templates

    def get_templates(self, command=None):
        """Returns the template metadata."""
        if command is None:
            return self.templates

        assert command in [GENERATE, INIT]
        return self.templates[command]


class RemoteIndexCollection:
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
            GENERATE: {},
            INIT: {}
        }
        for index in self.indexes:
            for command, temp in index.get_templates().items():
                templates[command].update(temp)
        return templates

    def get_templates(self, command=None):
        """Returns the template metadata."""
        if command is None:
            return self.templates

        assert command in [GENERATE, INIT]
        return self.templates[command]
