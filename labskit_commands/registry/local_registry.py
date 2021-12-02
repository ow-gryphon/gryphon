import shutil
from os import path
from .template_registry import TemplateRegistry, TEMPLATES_FOLDER


class LocalRegistry(TemplateRegistry):

    def __init__(self, registry_name: str, registry_path: str = ""):
        self.registry_folder = path.join(TEMPLATES_FOLDER, registry_name)
        self.registry_origin = registry_path

        assert len(self.registry_folder)
        assert path.isdir(self.registry_origin)

        if not path.isdir(self.registry_folder):
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
