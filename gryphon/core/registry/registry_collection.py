import logging
from pathlib import Path
from typing import List
from .template_registry import TemplateRegistry
from .local_registry import LocalRegistry
from .git_registry import GitRegistry

logger = logging.getLogger('gryphon')


class RegistryCollection:
    def __init__(self, registry_list: List[TemplateRegistry]):
        self.registry_list = registry_list

        full_metadata = {}
        for reg in self.registry_list:

            metadata = reg.get_templates()

            for command in metadata.keys():
                full_metadata.setdefault(command, {})
                command_metadata = metadata[command]
                # full_metadata[command].extend(command_metadata)

                for template in command_metadata.keys():
                    if template in full_metadata[command].keys():
                        raise ValueError(f"Duplicated template: \"{template}\"."
                                         f"Check your registries to deduplicate.")

                    full_metadata[command][template] = metadata[command][template]

        self.template_data = full_metadata

    def get_templates(self, command=None):
        """Returns the template metadata."""
        if command is None:
            return self.template_data

        return self.template_data.get(command, [])

    @classmethod
    def from_config_file(cls, settings, data_path: Path):

        local_registry = settings.get("local_registry", {})
        git_registry = settings.get("git_registry", {})

        template_registries = []

        # git ones
        for name, url in git_registry.items():
            reg = GitRegistry(
                registry_name=name,
                registry_url=url,
                registry_folder=data_path
            )
            template_registries.append(reg)

        # local ones
        for name, path in local_registry.items():
            path = Path(path)
            if not path.is_dir():
                logger.warning(f"Local template registry \"{path}\" was not found.")
                continue

            reg = LocalRegistry(
                registry_name=name,
                registry_origin=path,
                registry_folder=data_path
            )
            template_registries.append(reg)

        return cls(template_registries)
