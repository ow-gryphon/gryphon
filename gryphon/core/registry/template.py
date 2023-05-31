import os
import json
from pathlib import Path


class Template:
    def __init__(self, template_name, template_path, template_metadata, registry_type):

        self.name = template_name
        self.path = Path(template_path)

        self.template_index = template_path
        self.registry_type = registry_type

        self.command = template_metadata.get("command", "")
        self.display_name = template_metadata.get("display_name", self.name)
        self.keywords = template_metadata.get("keywords", [])
        self.methodology = template_metadata.get("methodology", [])
        self.sector = template_metadata.get("sector", [])
        self.topic = template_metadata.get("topic", [])
        self.arguments = template_metadata.get("arguments", [])
        self.read_more_link = template_metadata.get("read_more_link", "")
        self.force_env = template_metadata.get("force_env", False)

        self.dependencies = template_metadata.get("dependencies", [])
        self.description = template_metadata.get("description", "")
        self.version = template_metadata.get("version", "")
        
        self.ssh_domain = template_metadata.get("ssh_domain", None)
        self.repo_url = template_metadata.get("repo_url", None)
        
        # For init templates only
        self.shell_exec = template_metadata.get("shell_exec", None)
        self.addons = template_metadata.get("addons", None)
        

    @classmethod
    def template_from_path(cls, template_path: Path, type=""):

        with open(template_path / "metadata.json", "r", encoding="utf-8") as f:
            metadata = json.load(f)

        return cls(
            template_name=os.path.basename(template_path),
            template_path=template_path,
            template_metadata=metadata,
            registry_type=type
        )
