

class Template:
    def __init__(self, template_name, template_path, template_metadata):

        self.name = template_name
        self.path = template_path

        self.arguments = template_metadata.get("arguments", [])
        self.dependencies = template_metadata.get("dependencies", [])
        self.display_name = template_metadata.get("display_name", self.name)
