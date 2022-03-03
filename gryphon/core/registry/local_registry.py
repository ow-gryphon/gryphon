import shutil
from pathlib import Path
from .template_registry import TemplateRegistry


class LocalRegistry(TemplateRegistry):

    def __init__(self, registry_name: str, registry_origin: Path, registry_folder: Path):
        self.type = "local"
        self.name = registry_name

        self.registry_folder = registry_folder / registry_name
        self.registry_origin = registry_origin

        assert len(str(self.registry_folder))

        if self.registry_folder.is_dir():
            shutil.rmtree(self.registry_folder, ignore_errors=False)

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
            dirs_exist_ok=True,
            copy_function=shutil.copy,
            ignore=shutil.ignore_patterns(".git/**")
        )
