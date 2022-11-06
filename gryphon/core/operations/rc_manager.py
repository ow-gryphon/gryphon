import glob
import json
import logging
from datetime import datetime
from pathlib import Path

from ...constants import (
    GENERATE, INIT, GRYPHON_RC, CONDA, VENV, NB_STRIP_OUT, NB_EXTENSIONS, PRE_COMMIT_HOOKS
)

logger = logging.getLogger('gryphon')


class RCManager:

    # RC FILE
    @staticmethod
    def _get_key_rc(key, logfile=None):
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
                           f" gryphon_rc file at \"{logfile}\".")

    @staticmethod
    def _set_key_rc(key, value, logfile=None):
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
            f.write(json.dumps(new_contents, sort_keys=True, indent=4))
            f.truncate()

    @staticmethod
    def get_rc_file(folder=Path.cwd(), create=True):
        """
        Updates the needed options inside the .labskitrc file.
        """
        path = folder / GRYPHON_RC
        if path.is_file():
            return path

        if create:
            with open(path, "w", encoding="utf-8") as f:
                f.write("{}")

            return path
        else:
            raise FileNotFoundError("Could not find .gryphon_rc file inside folder.")

    # INITIALIZE
    @classmethod
    def initialize_log(cls, logfile=None):
        """
        Initialize the log file with require keys 
        """
        if logfile is None:
            raise FileNotFoundError("Could not find .gryphon_rc file inside folder.")

        with open(logfile, "r+", encoding="utf-8") as f:
            contents = json.load(f)

            new_contents = contents.copy()
            if "files" not in new_contents:
                new_contents["files"] = []

            if "operations" not in new_contents:
                new_contents["operations"] = []

            f.seek(0)
            f.write(json.dumps(new_contents, sort_keys=True, indent=4))
            f.truncate()

    # SET
    @classmethod
    def set_environment_manager(cls, environment_manager: str, logfile=None):
        """
        Add information about each and every file added to the project into the rc file.
        """
        assert environment_manager in [CONDA, VENV]
        cls._set_key_rc(key="environment_manager", value=environment_manager, logfile=logfile)

    @classmethod
    def set_environment_manager_path(cls, path: Path, logfile=None):
        """
        Add information about each and every file added to the project into the rc file.
        """
        cls._set_key_rc(key="environment_manager_path", value=str(path), logfile=logfile)

    @classmethod
    def set_handover_include_gryphon_generated_files(cls, state: bool, logfile=None):
        """
        Add information about each and every file added to the project into the rc file.
        """
        cls._set_key_rc(key="handover_include_gryphon_generated_files", value=state, logfile=logfile)

    @classmethod
    def set_handover_include_large_files(cls, state: bool, logfile=None):
        """
        Add information about each and every file added to the project into the rc file.
        """
        cls._set_key_rc(key="handover_include_large_files", value=state, logfile=logfile)

    @classmethod
    def set_addon_states(
            cls,
            install_nb_strip_out: bool = False,
            install_nbextensions: bool = False,
            install_pre_commit_hooks: bool = False,
            logfile=None
    ):
        """
        Add information about each and every file added to the project into the rc file.
        """
        cls._set_key_rc(key=NB_STRIP_OUT, value=install_nb_strip_out, logfile=logfile)
        cls._set_key_rc(key=NB_EXTENSIONS, value=install_nbextensions, logfile=logfile)
        cls._set_key_rc(key=PRE_COMMIT_HOOKS, value=install_pre_commit_hooks, logfile=logfile)

    # GET
    @classmethod
    def get_environment_manager_path(cls, logfile=None):
        """
        Add information about each and every file added to the project into the rc file.
        """
        return Path(cls._get_key_rc("environment_manager_path", logfile))

    @classmethod
    def get_environment_manager(cls, logfile=None):
        """
        Add information about each and every file added to the project into the rc file.
        """
        return cls._get_key_rc("environment_manager", logfile)

    @classmethod
    def get_gryphon_files(cls, logfile=None):
        """
        Add information about each and every file added to the project into the rc file.
        """
        return cls._get_key_rc("files", logfile)

    @classmethod
    def get_gryphon_operations(cls, logfile=None):
        """
        Add information about each and every file added to the project into the rc file.
        """
        return cls._get_key_rc("operations", logfile)

    @classmethod
    def get_handover_include_gryphon_generated_files(cls, logfile=None):
        """
        Add information about each and every file added to the project into the rc file.
        """
        return cls._get_key_rc("handover_include_gryphon_generated_files", logfile)

    @classmethod
    def get_handover_include_large_files(cls, logfile=None):
        """
        Add information about each and every file added to the project into the rc file.
        """
        return cls._get_key_rc("handover_include_large_files", logfile)

    # RC LOGS
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
            f.write(json.dumps(new_contents, sort_keys=True, indent=4))
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
                f.write(json.dumps(new_contents, sort_keys=True, indent=4))
                f.truncate()
        except FileNotFoundError:
            logger.warning(f"The {GRYPHON_RC} file was not found, therefore you are not inside a "
                           "Gryphon project directory.")

    @staticmethod
    def log_new_files(template, folder: Path, performed_action: str, logfile=None):
        """
        Add information about each and every file added to the project into the rc file.
        """
        assert performed_action in [INIT, GENERATE]
        if logfile is None:
            logfile = Path.cwd() / GRYPHON_RC

        files_and_folders = glob.glob(str(folder / "**"), recursive=True)

        files = list(filter(lambda x: x.is_file(), map(Path, files_and_folders)))

        with open(logfile, "r+", encoding="utf-8") as f:
            contents = json.load(f)

            new_contents = contents.copy()
            if "files" not in new_contents:
                new_contents["files"] = []

            for file in files:
                new_contents["files"].append(
                    dict(
                        path=str(file.relative_to(folder)),
                        template_name=template.name,
                        version=template.version,
                        action=performed_action,
                        created_at=str(datetime.now())
                    )
                )

            f.seek(0)
            f.write(json.dumps(new_contents, sort_keys=True, indent=4))
            f.truncate()
