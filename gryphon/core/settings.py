import json
import logging
import os
import shutil
from pathlib import Path

from .common_operations import (
    init_new_git_repo,
    initial_git_commit,
    get_current_python_version
)
from .operations.bash_utils import BashUtils
from .operations.environment_manager_operations import EnvironmentManagerOperations
from ..constants import (
    CONFIG_FILE, DEFAULT_CONFIG_FILE, DATA_PATH, SUCCESS,
    INIT, CONDA, DEFAULT_ENV, VENV, USE_LATEST, ALWAYS_ASK
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
    def change_template_version_policy(cls, policy):
        assert policy in [USE_LATEST, ALWAYS_ASK]
        with open(cls.get_config_path(), "r+", encoding="utf-8") as f:
            contents = json.load(f)
            contents["template_version_policy"] = policy

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

            contents["git_registry"] = default_settings.get("git_registry", {})
            contents["local_registry"] = default_settings.get("local_registry", {})

            f.seek(0)
            f.write(json.dumps(contents))
            f.truncate()

    @classmethod
    def add_local_template(cls, template_path):
        """Restore only the registries to the default."""
        with open(cls.get_config_path(), "r+", encoding="utf-8") as f:
            contents = json.load(f)
            contents.setdefault("local_templates", [])
            contents["local_templates"].append(template_path)

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

    @classmethod
    def test_template_cleanup(cls):
        pattern = "/sandbox/test_template"

        with open(cls.get_config_path(), "r+", encoding="utf-8") as f:
            contents = json.load(f)
            exclusion_list = []
            if "local_templates" in contents:
                for index, template_path in enumerate(contents["local_templates"]):
                    if pattern in template_path:
                        exclusion_list.append(index)

            for n in exclusion_list[::-1]:
                contents["local_templates"].pop(n)

            f.seek(0)
            f.write(json.dumps(contents))
            f.truncate()

    @classmethod
    def render_template_scaffolding(cls, location: Path):

        template_path = DATA_PATH / "template_scaffolding"
        python_version = get_current_python_version()

        with open(cls.get_config_path(), "r", encoding="UTF-8") as f:
            data = json.load(f)
            env_type = data.get("environment_management", DEFAULT_ENV)

        logger.info("Creating project scaffolding.")
        logger.info(f"Initializing project at {location}")

        # Files
        BashUtils.copy_project_template(
            template_destiny=Path(location),
            template_source=Path(template_path)
        )
        # TODO: JOIN ALL THE requirements.txt files in one at the time of project init with more than one zip file
        #  downloaded.

        # Git
        repo = init_new_git_repo(folder=location)
        initial_git_commit(repo)

        # ENV Manager
        if env_type == VENV:            # VENV
            EnvironmentManagerOperations.create_venv(folder=location, python_version=python_version)
        elif env_type == CONDA:
            # CONDA
            EnvironmentManagerOperations.create_conda_env(location, python_version=python_version)
            # install_extra_nbextensions_conda(location)
        else:
            raise RuntimeError("Invalid \"environment_management\" option on gryphon_config.json file."
                               f"Should be one of {[INIT, CONDA]} but \"{env_type}\" was given.")

        cls.add_local_template(str(Path(location).absolute()))
        logger.info("Added new template into the gryphon registry. You will be able to find it inside gryphon according"
                    " to the information given on metadata.json file.\n\n In order to find it on gryphon menus you will"
                    " have to fill the template information inside metadata.json file (providing at least the display "
                    "name and the command).")
        logger.log(SUCCESS, "Installation successful!")
