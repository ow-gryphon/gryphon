import json
import os
import re
from pathlib import Path

GRYPHON_FOLDER = Path("gryphon")

VERSION_PATTERN = re.compile(
    "^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)"
    "(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
)

context = json.loads(os.environ["GITHUB_CONTEXT"])
repo_name = context["repository"].split("/")[-1]
tag_name = context["event"]["ref"].split("/")[-1]


def execute_command(command) -> tuple:
    from subprocess import PIPE, Popen

    p = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    return stderr.decode(), stdout.decode()


with open(GRYPHON_FOLDER / "__init__.py", "r", encoding="UTF-8") as f:
    raw_text = f.read()

    version = raw_text.split('"')[-2]

try:
    # check if version on setup.py is equal to tag
    assert tag_name == version, f"Tag name \"{tag_name}\" doesn't match the version \"{version}\" from setup.py"

    # check if version is in the right format
    assert VERSION_PATTERN.match(version), f"Version on setup.py \"{tag_name}\" is not in the format 0.0.0 (X.X.X)"
    assert VERSION_PATTERN.match(tag_name), f"Tag name \"{tag_name}\" is not in the format 0.0.0 (X.X.X)"

except Exception as e:
    if VERSION_PATTERN.match(tag_name) and tag_name != version:
        # delete tag
        os.system(f"cd {GRYPHON_FOLDER} && git tag -d {tag_name} && git push --tags")
        os.system(f"cd {GRYPHON_FOLDER} && git push --delete origin {tag_name}")

        print(f"Use the command: \"git tag -d {tag_name}\" to remove the tag from your local repository.")

    raise e


# TODO: Check if conda can install some libraries (in order for conda to have the pip inside the newly created venv)
