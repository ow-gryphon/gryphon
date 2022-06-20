from .bash_utils import BashUtils
from .settings import SettingsManager
from ...logger import logger


class PreCommitManager:

    @staticmethod
    def install_pre_commit(environment_path, config_root):
        BashUtils.execute_and_log(
            f"cd \"{config_root}\" && \"{environment_path / 'bin' / 'pre-commit'}\" install"
        )

    @staticmethod
    def __replace_file_limit_on_config_file(location):
        file_size_limit_kb = int(SettingsManager.get_pre_commit_file_size_limit() * 1e3)
        yaml_file = location / '.pre-commit-config.yaml'
        with open(yaml_file, 'r+', encoding="UTF-8") as f:
            contents = f.read()

            contents = contents.replace('{{file_size_limit_kb}}', str(file_size_limit_kb))

            f.seek(0)
            f.write(contents)
            f.truncate()

    @classmethod
    def fill_configurations(cls, location):
        try:
            # every method that makes changes in the yaml file goes here
            cls.__replace_file_limit_on_config_file(location)

        except FileNotFoundError:
            logger.warning("Pre-commit config file '.pre-commit-config.yaml' not found in current folder.")

        # methods that doesn't change the .yaml can be kept outside the try clause
