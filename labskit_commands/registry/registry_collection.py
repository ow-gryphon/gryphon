from typing import List
from labskit_commands import registry


class RegistryCollection:
    def __init__(self, registry_list: List[registry.TemplateRegistry]):
        self.registry_list = registry_list

        full_metadata = {}
        for reg in self.registry_list:

            metadata = reg.get_metadata()

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

    @classmethod
    def from_config_file(cls, settings, data_path):

        local_registry = settings.get("local_registry", {})
        git_registry = settings.get("git_registry", {})

        template_registries = []

        # git ones
        for name, url in git_registry.items():
            reg = registry.GitRegistry(
                registry_name=name,
                registry_url=url,
                registry_folder=data_path
            )
            template_registries.append(reg)

        # local ones
        for name, path in local_registry.items():
            reg = registry.LocalRegistry(
                registry_name=name,
                registry_origin=path,
                registry_folder=data_path
            )
            template_registries.append(reg)

        return cls(template_registries)
