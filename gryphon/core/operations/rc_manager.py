import glob
import json
import logging
from datetime import datetime
from pathlib import Path

from ...constants import (
    GENERATE, INIT, CONFIG_FILE, DEFAULT_PYTHON_VERSION,
    USE_LATEST, GRYPHON_RC, CONDA, VENV
)

logger = logging.getLogger('gryphon')


class RCManager:

    # RC FILE
    @staticmethod
    def get_rc_file(folder=Path.cwd()):
        """
        Updates the needed options inside the .labskitrc file.
        """
        path = folder / GRYPHON_RC
        if path.is_file():
            return path

        with open(path, "w", encoding="utf-8") as f:
            f.write("{}")

        return path

    @staticmethod
    def log_new_files(template, performed_action: str, logfile=None):
        """
        Add information about each and every file added to the project into the rc file.
        """
        assert performed_action in [INIT, GENERATE]
        if logfile is None:
            logfile = Path.cwd() / GRYPHON_RC

        files_and_folders = glob.glob(str(template.path / "template" / "**"), recursive=True)
        files = list(filter(lambda x: x.is_file(), map(Path, files_and_folders)))

        with open(logfile, "r+", encoding="utf-8") as f:
            contents = json.load(f)

            new_contents = contents.copy()
            for file in files:
                new_contents.setdefault("files", []).append(
                    dict(
                        path=str(file.relative_to(template.path / "template")),
                        template_name=template.name,
                        version=template.version,
                        action=performed_action,
                        created_at=str(datetime.now())
                    )
                )

            f.seek(0)
            f.write(json.dumps(new_contents))
            f.truncate()

    @classmethod
    def set_environment_manager(cls, environment_manager: str, logfile=None):
        """
        Add information about each and every file added to the project into the rc file.
        """
        assert environment_manager in [CONDA, VENV]
        cls._set_key(key="environment_manager", value=environment_manager, logfile=logfile)

    @classmethod
    def set_environment_manager_path(cls, path: Path, logfile=None):
        """
        Add information about each and every file added to the project into the rc file.
        """
        cls._set_key(key="environment_manager_path", value=str(path), logfile=logfile)

    @staticmethod
    def _set_key(key, value, logfile=None):
        """
        Add information about each and every file added to the project into the rc file.
        """

        if logfile is None:
            logfile = Path.cwd() / GRYPHON_RC

        with open(logfile, "r+", encoding="utf-8") as f:
            contents = json.load(f)

            new_contents = contents.copy()
            new_contents[key] = value

            f.seek(0)
            f.write(json.dumps(new_contents))
            f.truncate()

    @classmethod
    def get_environment_manager_path(cls, logfile=None):
        """
        Add information about each and every file added to the project into the rc file.
        """
        return Path(cls._get_key("environment_manager_path", logfile))

    @classmethod
    def get_environment_manager(cls, logfile=None):
        """
        Add information about each and every file added to the project into the rc file.
        """
        return cls._get_key("environment_manager", logfile)

    @staticmethod
    def _get_key(key, logfile=None):
        """
        Add information about each and every file added to the project into the rc file.
        """
        if logfile is None:
            logfile = Path.cwd() / GRYPHON_RC

        with open(logfile, "r+", encoding="utf-8") as f:
            contents = json.load(f)

        try:
            return contents[key]
        except KeyError:
            raise KeyError(f"Could not find the key \"{key}\" in the contents \"{contents}\" read from the"
                           f" gryphon_rc file at {logfile}.")

    @staticmethod
    def log_operation(template, performed_action: str, logfile=None):
        """
        Add information about the operations made on the project into the rc file.
        """

        assert performed_action in [INIT, GENERATE]

        if logfile is None:
            logfile = Path.cwd() / GRYPHON_RC

        with open(logfile, "r+", encoding="utf-8") as f:
            contents = json.load(f)

            new_contents = contents.copy()
            if "operations" not in new_contents:
                new_contents["operations"] = []

            new_contents["operations"].append(
                dict(
                    template_name=template.name,
                    version=template.version,
                    action=performed_action,
                    created_at=str(datetime.now())
                )
            )

            f.seek(0)
            f.write(json.dumps(new_contents))
            f.truncate()

    @staticmethod
    def log_add_library(libraries: list, logfile=None):
        """
        Add information about installed inside the project into the rc file.
        """
        if logfile is None:
            logfile = Path.cwd() / GRYPHON_RC
        try:
            with open(logfile, "r+", encoding="utf-8") as f:
                contents = json.load(f)

                new_contents = contents.copy()
                if "libraries" not in new_contents:
                    new_contents["libraries"] = []

                for lib in libraries:
                    new_contents["libraries"].append(
                        dict(
                            name=lib,
                            added_at=str(datetime.now())
                        )
                    )

                f.seek(0)
                f.write(json.dumps(new_contents))
                f.truncate()
        except FileNotFoundError:
            logger.warning(f"The {GRYPHON_RC} file was not found, therefore you are not inside a "
                           "Gryphon project directory.")

    @staticmethod
    def get_current_python_version():
        """
        Recovers the current python version from the config file.
        """
        with open(CONFIG_FILE, "r", encoding="UTF-8") as f:
            return json.load(f).get(
                "default_python_version",
                DEFAULT_PYTHON_VERSION
            )

    @staticmethod
    def get_current_template_version_policy():
        """
        Recovers the current template version policy from the config file.
        """
        with open(CONFIG_FILE, "r", encoding="UTF-8") as f:
            return json.load(f).get(
                "template_version_policy",
                USE_LATEST
            )
