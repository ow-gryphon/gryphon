import os
import json
import logging
import shutil
from pathlib import Path
from ..constants import (
    CONFIG_FILE, DEFAULT_CONFIG_FILE, DATA_PATH,
    INIT, CONDA, DEFAULT_ENV, VENV
)
from .common_operations import (
    copy_project_template,
    create_venv,
    init_new_git_repo,
    initial_git_commit,
    create_conda_env,
    get_current_python_version
)

logger = logging.getLogger('gryphon')


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
    def change_default_python_version(cls, python_version):

        with open(cls.get_config_path(), "r+", encoding="utf-8") as f:
            contents = json.load(f)
            contents["default_python_version"] = python_version

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

            contents.setdefault("git_registry", {})
            contents.setdefault("local_registry", {})

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

    @staticmethod
    def render_template_scaffolding(location: Path):

        template_path = DATA_PATH / "template_scaffolding"
        python_version = get_current_python_version()

        with open(SettingsManager.get_config_path(), "r", encoding="UTF-8") as f:
            data = json.load(f)
            env_type = data.get("environment_management", DEFAULT_ENV)

        logger.info("Creating project scaffolding.")
        logger.info(f"Initializing project at {location}")

        # Files
        copy_project_template(
            template_destiny=Path(location),
            template_source=Path(template_path)
        )

        # Git
        repo = init_new_git_repo(folder=location)
        initial_git_commit(repo)

        # ENV Manager
        if env_type == VENV:            # VENV
            create_venv(folder=location, python_version=python_version)
        elif env_type == CONDA:
            # CONDA
            create_conda_env(location, python_version=python_version)
            # install_extra_nbextensions_conda(location)
        else:
            raise RuntimeError("Invalid \"environment_management\" option on gryphon_config.json file."
                               f"Should be one of {[INIT, CONDA]} but \"{env_type}\" was given.")
