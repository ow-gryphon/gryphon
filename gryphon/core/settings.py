import json
import os
import shutil
from ..constants import CONFIG_FILE, DEFAULT_CONFIG_FILE


class SettingsManager:

    def __init__(self):
        """
        init method empty because the class is
        only meant to create a namespace for its methods
        """

    @classmethod
    def restore_default_config_file(cls):
        os.remove(cls.get_config_path())
        shutil.copy(
            src=DEFAULT_CONFIG_FILE,
            dst=cls.get_config_path()
        )

    @classmethod
    def change_environment_manager(cls, environment_manager):

        with open(cls.get_config_path(), "r+", encoding="utf-8") as f:
            contents = json.load(f)
            contents["environment_management"] = environment_manager

            f.seek(0)
            f.write(json.dumps(contents))
            f.truncate()

    @classmethod
    def add_git_template_registry(cls, registry_repo, registry_name):

        with open(cls.get_config_path(), "r+", encoding="utf-8") as f:
            contents = json.load(f)
            contents["git_registry"][registry_name] = registry_repo

            f.seek(0)
            f.write(json.dumps(contents))
            f.truncate()

    @classmethod
    def add_local_template_registry(cls, registry_path, registry_name):

        with open(cls.get_config_path(), "r+", encoding="utf-8") as f:
            contents = json.load(f)
            contents["local_registry"][registry_name] = registry_path

            f.seek(0)
            f.write(json.dumps(contents))
            f.truncate()

    @classmethod
    def remove_template_registry(cls, registry_name):
        """Removes a given registry from the config file"""

        with open(cls.get_config_path(), "r+", encoding="utf-8") as f:
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

    @classmethod
    def restore_registries(cls):
        """Restore only the registries to the default."""
        with open(DEFAULT_CONFIG_FILE, "r", encoding="utf-8") as f:
            default_settings = json.load(f)

        with open(cls.get_config_path(), "r+", encoding="utf-8") as f:
            contents = json.load(f)
            contents["git_registry"] = default_settings["git_registry"]
            contents["local_registry"] = default_settings["local_registry"]

            f.seek(0)
            f.write(json.dumps(contents))
            f.truncate()

    @classmethod
    def list_template_registries(cls):
        with open(cls.get_config_path(), "r", encoding="utf-8") as f:
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

    @staticmethod
    def get_config_path():
        """
        Method that returns the config file path
        It makes it easier too change later and also easier to mock in tests
        """
        return CONFIG_FILE
