import glob
import json
import os
from pathlib import Path
from typing import List, Dict

import git
from git import Repo

from .template import Template
from .versioned_template import VersionedTemplate
from ..operations.bash_utils import BashUtils
from ...constants import GRYPHON_HOME, GENERATE, INIT, REMOTE_INDEX
from ...logger import logger


class RemoteIndex:
    def __init__(self, index_url: str, index_repo: str, index_name: str):
        self.index_url = index_url
        self.index_repo = index_repo
        self.index_local_path = GRYPHON_HOME / "index" / index_name

        if not self.index_local_path.is_dir():
            os.makedirs(self.index_local_path)
        else:
            BashUtils.remove_folder(self.index_local_path)

        try:
            self.repo = Repo.clone_from(self.index_repo, self.index_local_path)
        except git.exc.GitCommandError:
            logger.warning(f"Failed to get index: {self.index_url}\nNo template from this index will be available.")
            logger.debug(f"Failed to get index: {self.index_url}")
            self.templates = {}

            return

        self.templates = self.generate_templates()

    # def read_index_metadata(self) -> Dict[str, List]:
    #     metadata_files = glob.glob(str(self.index_local_path / "**" / "metadata.json"), recursive=True)
    #     metadata_contents = {
    #         GENERATE: [],
    #         INIT: []
    #     }
    #     for file in metadata_files:
    #         with open(file, "r", encoding="UTF-8") as f:
    #             contents = json.load(f)
    #             if type(contents) != list:
    #                 continue
    #
    #             versions = list(map(lambda x: x["version"], contents))
    #
    #             latest_version = sort_versions(versions)[-1]
    #             latest = list(filter(lambda x: x["version"] == latest_version, contents))[0]
    #
    #             latest["path"] = Path(file).parent
    #
    #             command = latest["command"]
    #             assert command in [GENERATE, INIT]
    #             metadata_contents[command].append(contents)
    #
    #     return metadata_contents

    def generate_templates(self) -> Dict[str, Dict[str, Template]]:
        metadata_files = glob.glob(
            str(self.index_local_path / "**" / "metadata.json"),
            recursive=True
        )

        template_versions = {}
        for file in metadata_files:
            # for each template folder inside index
            with open(file, "r", encoding="UTF-8") as f:
                metadata = json.load(f)

            if type(metadata) != list:
                continue

            path = Path(file).parent
            name = path.parts[-1]
            template_versions[name] = VersionedTemplate(
                metadata,
                template_name=name,
                template_path=self.index_url,
                registry_type=REMOTE_INDEX
            )

        templates = {
            GENERATE: {},
            INIT: {}
        }

        for name, template in template_versions.items():
            assert template.command in [INIT, GENERATE]
            templates[template.command][name] = template

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
