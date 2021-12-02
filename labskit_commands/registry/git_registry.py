from os import path
import git
from .template_registry import TemplateRegistry, TEMPLATES_FOLDER


class GitRegistry(TemplateRegistry):

    def __init__(self, registry_name: str, registry_url: str = ""):
        self.registry_folder = path.join(TEMPLATES_FOLDER, registry_name)

        if not path.isdir(self.registry_folder):
            if registry_url != "":
                self.repository = git.Repo.clone_from(
                    url=registry_url,
                    to_path=self.registry_folder
                )
        else:
            self.repository = git.Repo(self.registry_folder)
            assert not self.repository.bare
            self.update_registry()

        super().__init__(templates_path=self.registry_folder)

    def update_registry(self):
        """Updates the template registry to the latest remote one."""
        remote = self.repository.remote()
        remote.pull()
