import shutil
from os import path
from .template_registry import TemplateRegistry
from labskit_commands.command_operations import remove_folder


class LocalRegistry(TemplateRegistry):

    def __init__(self, registry_name: str, registry_origin: str, registry_folder):
        self.registry_folder = path.join(registry_folder, registry_name)
        self.registry_origin = registry_origin

        assert len(self.registry_folder)
        assert path.isdir(self.registry_origin)

        if path.isdir(self.registry_folder):
            remove_folder(self.registry_folder)

        self._copy_registry()
        super().__init__(templates_path=self.registry_folder)

    def update_registry(self):
        """Updates the template registry to the latest changes in local folder."""
        self._copy_registry()

    def _copy_registry(self):
        """Updates the template registry to the latest changes in local folder."""
        shutil.copytree(
            src=self.registry_origin,
            dst=self.registry_folder,
            dirs_exist_ok=True
        )
