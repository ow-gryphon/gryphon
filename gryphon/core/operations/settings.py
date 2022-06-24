import json
import logging
import os
import shutil

from ...constants import (
    CONFIG_FILE, DEFAULT_CONFIG_FILE, VENV, USE_LATEST, ALWAYS_ASK,
    DEFAULT_PYTHON_VERSION
)

logger = logging.getLogger('gryphon')


class SettingsManager:

    def __init__(self):
        """
        init method empty because the class is
        only meant to create a namespace for its methods
        """

    @staticmethod
    def get_config_path():
        """
        Method that returns the config file path
        It makes it easier too change later and also easier to mock in tests
        """
        return CONFIG_FILE

    @classmethod
    def _set_key(cls, key, value):
        """Restore only the registries to the default."""
        with open(cls.get_config_path(), "r+", encoding="utf-8") as f:
            contents = json.load(f)
            contents[key] = value

            f.seek(0)
            f.write(json.dumps(contents))
            f.truncate()

    @classmethod
    def _get_key(cls, key, default=None):
        with open(cls.get_config_path(), "r", encoding="utf-8") as f:
            contents = json.load(f)

        try:
            return contents[key]
        except KeyError:
            if default is None:
                raise KeyError(f"Could not find the given key (\"{key}\") in the current config file.")
            else:
                return default

    @classmethod
    def restore_default_config_file(cls):
        os.remove(cls.get_config_path())
        shutil.copy(
            src=DEFAULT_CONFIG_FILE,
            dst=cls.get_config_path()
        )

    @classmethod
    def change_environment_manager(cls, environment_manager):
        cls._set_key("environment_management", environment_manager)

    @classmethod
    def change_handover_file_size_limit(cls, limit: float):
        cls._set_key("handover_file_size_limit", limit)

    @classmethod
    def change_handover_include_gryphon_generated_files(cls, state: bool):
        cls._set_key("handover_include_gryphon_generated_files", state)

    @classmethod
    def change_default_python_version(cls, python_version):
        cls._set_key("default_python_version", python_version)

    @classmethod
    def change_template_version_policy(cls, policy):
        assert policy in [USE_LATEST, ALWAYS_ASK]
        cls._set_key("template_version_policy", policy)

    @classmethod
    def add_git_template_registry(cls, registry_repo, registry_name):
        git_registry = cls._get_key("git_registry")
        git_registry[registry_name] = registry_repo
        cls._set_key("git_registry", git_registry)

    @classmethod
    def add_local_template_registry(cls, registry_path, registry_name):
        local_registry = cls._get_key("local_registry")
        local_registry[registry_name] = registry_path
        cls._set_key("local_registry", local_registry)

    @classmethod
    def remove_template_registry(cls, registry_name):
        """Removes a given registry from the config file"""
        git_registry = cls._get_key("git_registry")
        local_registry = cls._get_key("local_registry")

        if registry_name in git_registry:
            git_registry.pop(registry_name)
            cls._set_key("git_registry", git_registry)

        elif registry_name in local_registry:
            local_registry.pop(registry_name)
            cls._set_key("local_registry", local_registry)

        else:
            raise RuntimeError("Registry name was not found on config file.")

    @classmethod
    def restore_registries(cls):
        """Restore only the registries to the default."""
        with open(DEFAULT_CONFIG_FILE, "r", encoding="utf-8") as f:
            default_settings = json.load(f)

        cls._set_key("git_registry", default_settings.get("git_registry", {}))
        cls._set_key("local_registry", default_settings.get("local_registry", {}))

    @classmethod
    def add_local_template(cls, template_path):
        """Restore only the registries to the default."""
        local_templates = cls._get_key("local_templates")
        local_templates.append(template_path)
        cls._set_key("local_templates", local_templates)

    @classmethod
    def list_template_registries(cls):

        git_registry = cls._get_key("git_registry")
        local_registry = cls._get_key("local_registry")

        git_registries = {
            name: "git"
            for name in git_registry.keys()
        }

        local_registries = {
            name: "local"
            for name in local_registry.keys()
        }

        git_registries.update(local_registries)
        return git_registries

    @classmethod
    def get_environment_manager(cls):
        return cls._get_key("environment_management")

    @classmethod
    def get_handover_file_size_limit(cls):
        return cls._get_key("handover_file_size_limit")

    @classmethod
    def get_handover_include_large_files(cls) -> bool:
        return cls._get_key("handover_include_large_files")

    @classmethod
    def get_handover_include_gryphon_generated_files(cls):
        return cls._get_key("handover_include_gryphon_generated_files")

    @classmethod
    def test_template_cleanup(cls):
        local_templates = cls._get_key("local_templates", [])

        pattern = "/sandbox/test_template"

        exclusion_list = []
        if local_templates:
            for index, template_path in enumerate(local_templates):
                if pattern in template_path:
                    exclusion_list.append(index)

        for n in exclusion_list[::-1]:
            local_templates.pop(n)

        cls._set_key("local_templates", local_templates)

    # CONFIG FILE
    @classmethod
    def get_current_python_version(cls):
        """
        Recovers the current python version from the config file.
        """
        return cls._get_key("default_python_version", DEFAULT_PYTHON_VERSION)

    @classmethod
    def get_handover_include_gryphon_generated_files(cls):
        """
        Recovers the current python version from the config file.
        """
        return cls._get_key("handover_include_gryphon_generated_files", DEFAULT_PYTHON_VERSION)

    @classmethod
    def get_current_template_version_policy(cls):
        """
        Recovers the current template version policy from the config file.
        """

        return cls._get_key("template_version_policy", USE_LATEST)

    @classmethod
    def get_current_environment_manager(cls):
        """
        Recovers the current template version policy from the config file.
        """
        return cls._get_key("environment_manager", VENV)
