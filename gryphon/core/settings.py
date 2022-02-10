import json
import os
import shutil
from ..constants import CONFIG_FILE, DEFAULT_CONFIG_FILE


class SettingsManager:

    def __init__(self):
        pass

    @staticmethod
    def restore_default_config_file():
        os.remove(CONFIG_FILE)
        shutil.copy(
            src=DEFAULT_CONFIG_FILE,
            dst=CONFIG_FILE
        )

    @staticmethod
    def change_environment_manager(environment_manager):

        with open(CONFIG_FILE, "r+", encoding="utf-8") as f:
            contents = json.load(f)
            contents["environment_management"] = environment_manager

            f.seek(0)
            f.write(json.dumps(contents))
            f.truncate()

    @staticmethod
    def add_git_template_registry(registry_repo, registry_name):

        with open(CONFIG_FILE, "r+", encoding="utf-8") as f:
            contents = json.load(f)
            contents["git_registry"][registry_name] = registry_repo

            f.seek(0)
            f.write(json.dumps(contents))
            f.truncate()

    @staticmethod
    def add_local_template_registry(registry_path, registry_name):

        with open(CONFIG_FILE, "r+", encoding="utf-8") as f:
            contents = json.load(f)
            contents["local_registry"][registry_name] = registry_path

            f.seek(0)
            f.write(json.dumps(contents))
            f.truncate()

    @staticmethod
    def remove_template_registry(registry_name):
        """Removes a given registry from the config file"""

        with open(CONFIG_FILE, "r+", encoding="utf-8") as f:
            contents = json.load(f)

            if registry_name in contents["git_registry"]:
                contents["git_registry"].pop(registry_name)
            elif registry_name in contents["local_registry"]:
                contents["local_registry"].pop(registry_name)
            else:
                raise RuntimeError("Registry name was not found on config file.")

            f.seek(0)
            f.write(json.dumps(contents))
            f.truncate()

    @staticmethod
    def restore_registries():
        """Restore only the registries to the default."""
        with open(DEFAULT_CONFIG_FILE, "r", encoding="utf-8") as f:
            default_settings = json.load(f)

        with open(CONFIG_FILE, "r+", encoding="utf-8") as f:
            contents = json.load(f)
            contents["git_registry"] = default_settings["git_registry"]
            contents["local_registry"] = default_settings["local_registry"]

            f.seek(0)
            f.write(json.dumps(contents))
            f.truncate()

    @staticmethod
    def list_template_registries():
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            contents = json.load(f)

        git_registries = {
            name: "git"
            for name in contents["git_registry"].keys()
        }

        local_registries = {
            name: "local"
            for name in contents["local_registry"].keys()
        }

        git_registries.update(local_registries)
        return git_registries

# TODO: power user to create a bare bones gryphon template.
