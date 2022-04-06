from .template import Template
from ..common_operations import sort_versions
from ...constants import LATEST


class VersionedTemplate:

    def __init__(self, template_metadata, template_name, template_path, registry_type):
        self.templates = [
            Template(
                template_metadata=metadata,
                template_name=template_name,
                template_path=template_path,
                registry_type=registry_type
            )
            for metadata in template_metadata
        ]

        self.available_versions = list(map(lambda x: x["version"], template_metadata))
        latest_version = sort_versions(self.available_versions)[-1]
        self.latest = self[latest_version]

        # self.name = template_name
        # self.registry_type = registry_type
        # self.command = self.latest.command
        # self.display_name = self.latest.display_name
        # self.keywords = self.latest.keywords
        # self.methodology = self.latest.methodology
        # self.sector = self.latest.sector
        # self.topic = self.latest.topic

    def __getattr__(self, item):
        """
        If the following syntax occurs:

        >>> temp = VersionedTemplate(...)
        >>> print(temp.name)

        The name gathered will be retrivied from inside the latest version by default

        """
        return getattr(self.latest, item)

    def __getitem__(self, item) -> Template:
        """
        If it is necessary to choose an specific version, it can be obtained using
        the following syntax:

        >>> temp = VersionedTemplate(...)
        >>> print(temp["v0.0.2"])

        """
        if item == LATEST:
            return self.latest

        filtered = list(filter(lambda x: x.version == item, self.templates))
        if len(filtered) == 1:
            return filtered[0]

        elif len(filtered) > 1:
            raise RuntimeError(f"More than one template corresponded to the version asked ({item})."
                               f"It is likely to be a problem in the metadata indexing system."
                               f"Please call the support.")
        else:
            raise KeyError(f"Could not find version \"{item}\"")
