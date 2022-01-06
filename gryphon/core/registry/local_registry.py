import shutil
from pathlib import Path
from .template_registry import TemplateRegistry
from ..command_operations import remove_folder


class LocalRegistry(TemplateRegistry):

    def __init__(self, registry_name: str, registry_origin: Path, registry_folder: Path):
        self.registry_folder = registry_folder / registry_name
        self.registry_origin = registry_origin

        assert len(str(self.registry_folder))
        assert self.registry_origin.is_dir()

        if self.registry_folder.is_dir():
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
