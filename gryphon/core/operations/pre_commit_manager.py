import platform
import shutil

from .bash_utils import BashUtils
from .rc_manager import RCManager
from .settings import SettingsManager
from ...logger import logger
from ...constants import DATA_PATH, PRE_COMMIT_YML, CONDA, VENV, GRYPHON_RC


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
    def _activate_hooks(environment_path):
        BashUtils.execute_and_log(f"\"{environment_path / 'bin' / 'pre-commit'}\" install")

    @staticmethod
    def _install_pre_commit(env_manager, environment_path):

        if env_manager == CONDA:
            BashUtils.execute_and_log(f'conda install pre-commit --prefix \"{environment_path}\"')

        elif env_manager == VENV:

            if platform.system() == "Windows":
                BashUtils.execute_and_log(f'\"{environment_path / "bin" / "pip"}\" install pre-commit')

            else:
                BashUtils.execute_and_log(f'\"{environment_path / "Scripts" / "pip"}\" install pre-commit')

    @classmethod
    def initial_setup(cls, location):
        shutil.copy(
            src=DATA_PATH / PRE_COMMIT_YML,
            dst=location
        )
        cls._fill_configurations(location)

    @classmethod
    def final_setup(cls, location):

        log = location / GRYPHON_RC
        env_manager = RCManager.get_environment_manager(logfile=log)
        environment_path = RCManager.get_environment_manager_path(logfile=log)

        cls._install_pre_commit(env_manager, environment_path)
        cls._activate_hooks(environment_path)
