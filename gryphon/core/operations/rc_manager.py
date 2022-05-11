import glob
import json
import logging
from datetime import datetime
from pathlib import Path

from ...constants import (
    GENERATE, INIT, CONFIG_FILE, DEFAULT_PYTHON_VERSION,
    USE_LATEST, GRYPHON_HISTORY
)

logger = logging.getLogger('gryphon')


class RCManager:

    # RC FILE
    @staticmethod
    def get_rc_file(folder=Path.cwd()):
        """
        Updates the needed options inside the .labskitrc file.
        """
        path = folder / GRYPHON_HISTORY
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
            logfile = Path.cwd() / GRYPHON_HISTORY

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

    @staticmethod
    def log_operation(template, performed_action: str, logfile=None):
        """
        Add information about the operations made on the project into the rc file.
        """

        assert performed_action in [INIT, GENERATE]

        if logfile is None:
            logfile = Path.cwd() / GRYPHON_HISTORY

        with open(logfile, "r+", encoding="utf-8") as f:
            contents = json.load(f)

            new_contents = contents.copy()
            new_contents.setdefault("operations", []).append(
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
            logfile = Path.cwd() / GRYPHON_HISTORY
        try:
            with open(logfile, "r+", encoding="utf-8") as f:
                contents = json.load(f)

                new_contents = contents.copy()
                for lib in libraries:
                    new_contents.setdefault("libraries", []).append(
                        dict(
                            name=lib,
                            added_at=str(datetime.now())
                        )
                    )

                f.seek(0)
                f.write(json.dumps(new_contents))
                f.truncate()
        except FileNotFoundError:
            logger.warning("The .gryphon_history file was not found, therefore you are not inside a "
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
