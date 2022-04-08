import shutil
from typing import List
from pathlib import Path
from .template_registry import TemplateRegistry


class LocalRegistry(TemplateRegistry):

    def __init__(self, registry_name: str,
                 templates_root: Path = None, template_paths: List[Path] = None):
        self.type = "local"
        self.name = registry_name

        # self.registry_folder = registry_folder / registry_name
        self.registry_folder = self.registry_origin = templates_root

        assert len(str(self.registry_folder))

        # if self.registry_folder.is_dir():
        #     shutil.rmtree(self.registry_folder, ignore_errors=False)

        # self._copy_registry()
        super().__init__(
            templates_root=templates_root,
            template_paths=template_paths
        )

    def update_registry(self):
        """Updates the template registry to the latest changes in local folder."""
        # self._copy_registry()

    def _copy_registry(self):
        """Updates the template registry to the latest changes in local folder."""
        shutil.copytree(
            src=self.registry_origin,
            dst=self.registry_folder,
            dirs_exist_ok=True,
            copy_function=shutil.copy,
            ignore=shutil.ignore_patterns(".git/**")
        )
