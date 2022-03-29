import os
import re
import json
from pathlib import Path


INDEX_FILE = "grypi/index.html"
VERSION_PATTERN = re.compile(
    "^v(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)"
    "(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$")


def get_metadata_path(package_name):
    return Path("template") / package_name / "metadata.json"


def read_metadata(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    # Get the context from the environment variable
    context = json.loads(os.environ["GITHUB_CONTEXT"])
    repo_name = context["repository"].split("/")[-1]
    tag_name = context["event"]["ref"].split("/")[-1]

    if not VERSION_PATTERN.match(tag_name):
        raise RuntimeError(f"Version name not valid: {tag_name}")

    metadata_file = f"template/metadata.json"
    version_metadata = read_metadata(metadata_file)
    metadata_path = get_metadata_path(repo_name)

    if not metadata_path.is_file():
        metadata = {
            tag_name: version_metadata
        }

        with open(metadata_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(metadata))

    else:
        with open(metadata_path, "r+", encoding="utf-8") as f:
            metadata = json.load(f)
            metadata[tag_name] = version_metadata

            f.seek(0)
            f.write(json.dumps(metadata))
            f.truncate()


if __name__ == "__main__":
    main()
