from typing import List
from .template_registry import TemplateRegistry


class RegistryCollection:
    def __init__(self, registry_list: List[TemplateRegistry]):
        self.registry_list = registry_list

        full_metadata = {}
        for registry in self.registry_list:

            metadata = registry.get_metadata()

            for command in metadata.keys():
                full_metadata.setdefault(command, {})
                command_metadata = metadata[command]

                for template in command_metadata.keys():
                    if template in full_metadata[command].keys():
                        raise ValueError(f"Duplicated template: \"{template}\"."
                                         f"Check your registries to deduplicate.")

                    full_metadata[command][template] = metadata[command][template]

        self.metadata = full_metadata

    def get_metadata(self):
        return self.metadata
