from .template import Template
from ..common_operations import sort_versions
from ...constants import LATEST


class VersionedTemplate:

    def __init__(self, template_name, template_path, template_metadata, registry_type):
        self.name = template_name
        self.registry_type = registry_type

        self.versions = {}
        for version, metadata in template_metadata.items():
            self.versions[version] = Template(
                template_name=template_name,
                template_path=template_path,
                template_metadata=metadata,
                registry_type=registry_type
            )

        self.available_versions = list(template_metadata.keys())
        latest_version = sort_versions(self.available_versions)[-1]
        self.versions[LATEST] = self.versions[latest_version]

        self.command = self.versions[LATEST].command
        self.display_name = self.versions[LATEST].display_name
        self.keywords = self.versions[LATEST].keywords
        self.methodology = self.versions[LATEST].methodology
        self.sector = self.versions[LATEST].sector
        self.topic = self.versions[LATEST].topic

    def __getitem__(self, item):
        return self.versions[item]
