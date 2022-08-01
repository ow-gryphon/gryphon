import platform
import shutil

from .bash_utils import BashUtils
from .rc_manager import RCManager
from .settings import SettingsManager
from ...constants import DATA_PATH, PRE_COMMIT_YML, GRYPHON_RC
from ...logger import logger


class PreCommitManager:

    @staticmethod
    def __replace_file_limit_on_config_file(location):
        file_size_limit_kb = int(SettingsManager.get_pre_commit_file_size_limit() * 1e3)
        yaml_file = location / PRE_COMMIT_YML
        with open(yaml_file, 'r+', encoding="UTF-8") as f:
            contents = f.read()

            contents = contents.replace('{{file_size_limit_kb}}', str(file_size_limit_kb))

            f.seek(0)
            f.write(contents)
            f.truncate()

    @classmethod
    def _fill_configurations(cls, location):
        try:
            # every method that makes changes in the yaml file goes here
            cls.__replace_file_limit_on_config_file(location)

        except FileNotFoundError:
            logger.warning("Pre-commit config file '.pre-commit-config.yaml' not found in current folder.")

        # methods that doesn't change the .yaml can be kept outside the try clause

    @staticmethod
    def _activate_hooks(environment_path, git_repo_root):
        sub_folder = 'bin'

        if platform.system() == "Windows":
            sub_folder = 'Scripts'

        BashUtils.execute_and_log(
            f"cd \"{git_repo_root}\" && \"{environment_path / sub_folder / 'pre-commit'}\" install"
        )

    @staticmethod
    def _install_pre_commit(environment_path):

        if platform.system() == "Windows":
            BashUtils.execute_and_log(f'\"{environment_path / "Scripts" / "pip"}\" install pre-commit '
                                      f'--no-warn-script-location')
        else:
            BashUtils.execute_and_log(f'\"{environment_path / "bin" / "pip"}\" install pre-commit')

    @classmethod
    def initial_setup(cls, location):
        shutil.copy(
            src=DATA_PATH / PRE_COMMIT_YML,
            dst=location
        )
        cls._fill_configurations(location)

    @classmethod
    def final_setup(cls, location, environment_path=None):

        log = location / GRYPHON_RC
        if environment_path is None:
            environment_path = RCManager.get_environment_manager_path(logfile=log)

        cls._install_pre_commit(environment_path)
        cls._activate_hooks(environment_path, location)
