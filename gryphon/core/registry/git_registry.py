from pathlib import Path
import git
from ..logger import Logging
from .template_registry import TemplateRegistry


class GitRegistry(TemplateRegistry):

    def __init__(self, registry_name: str, registry_url: str, registry_folder: Path):
        self.registry_folder = registry_folder / registry_name
        self.registry_url = registry_url
        if not self.registry_folder.is_dir():
            if registry_url != "":
                self.repository = git.Repo.clone_from(
                    url=self.registry_url,
                    to_path=self.registry_folder
                )
        else:
            self.repository = git.Repo(self.registry_folder)
            assert not self.repository.bare
            self.update_registry()

        super().__init__(templates_path=self.registry_folder)

    def update_registry(self):
        """Updates the template registry to the latest remote one."""
        try:
            remote = self.repository.remote()
            remote.pull()
        except git.exc.GitCommandError:
            Logging.warn(f"Failed to update template repository: {self.registry_url}")
