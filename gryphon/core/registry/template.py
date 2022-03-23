import os
import json
from pathlib import Path


class Template:
    def __init__(self, template_name, template_path, template_metadata):

        self.name = template_name
        self.path = Path(template_path)

        self.template_index = template_path
        self.command = template_metadata.get("command", "")

        self.arguments = template_metadata.get("arguments", [])
        self.dependencies = template_metadata.get("dependencies", [])
        self.display_name = template_metadata.get("display_name", self.name)
        self.description = template_metadata.get("description", "")
        self.methodology = template_metadata.get("methodology", [])
        self.sector = template_metadata.get("sector", [])
        self.topic = template_metadata.get("topic", [])
        self.keywords = template_metadata.get("keywords", [])
        self.version = template_metadata.get("version", "")

    @classmethod
    def template_from_path(cls, template_path: Path):

        with open(template_path / "metadata.json", "r", encoding="utf-8") as f:
            metadata = json.load(f)

        return cls(
            template_name=os.path.basename(template_path),
            template_path=template_path,
            template_metadata=metadata
        )
