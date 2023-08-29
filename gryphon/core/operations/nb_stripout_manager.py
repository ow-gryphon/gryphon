import platform

from .bash_utils import BashUtils
from .rc_manager import RCManager
from ...constants import GRYPHON_RC


class NBStripOutManager:

    @staticmethod
    def _install_nb_strip_out(environment_path):

        if platform.system() == "Windows":
            BashUtils.execute_and_log(f'\"{environment_path / "Scripts" / "pip"}\" install nbstripout '
                                      f'--no-warn-script-location --disable-pip-version-check')
        else:
            return_code, output = BashUtils.execute_and_log(
                f'\"{environment_path / "bin" / "pip"}\" install nbstripout '
                f'--disable-pip-version-check')

            # On some installations on Unix systems, only pip3 is available
            if return_code == 127:
                BashUtils.execute_and_log(
                    f'\"{environment_path / "bin" / "pip3"}\" install nbstripout '
                    f'--disable-pip-version-check')

    @staticmethod
    def _uninstall_nb_strip_out(environment_path):

        if platform.system() == "Windows":
            BashUtils.execute_and_log(f'\"{environment_path / "Scripts" / "pip"}\" uninstall nbstripout -y'
                                      f'--no-warn-script-location --disable-pip-version-check')
        else:
            return_code, output = BashUtils.execute_and_log(
                f'\"{environment_path / "bin" / "pip"}\" uninstall nbstripout -y'
                f' --disable-pip-version-check')

            # On some installations on Unix systems, only pip3 is available
            if return_code == 127:
                BashUtils.execute_and_log(
                    f'\"{environment_path / "bin" / "pip3"}\" uninstall nbstripout -y'
                    f' --disable-pip-version-check')

    @staticmethod
    def _activate_nb_strip_out(environment_path, git_repo_root):
        sub_folder = 'bin'

        if platform.system() == "Windows":
            sub_folder = 'Scripts'

        BashUtils.execute_and_log(
            f"cd \"{git_repo_root}\" && \"{environment_path / sub_folder / 'nbstripout'}\" install"
        )

    @staticmethod
    def _deactivate_nb_strip_out(environment_path, git_repo_root):
        sub_folder = 'bin'

        if platform.system() == "Windows":
            sub_folder = 'Scripts'

        BashUtils.execute_and_log(
            f"cd \"{git_repo_root}\" && \"{environment_path / sub_folder / 'nbstripout'}\" --uninstall"
        )

    @classmethod
    def setup(cls, location, environment_path=None):

        log = location / GRYPHON_RC
        if environment_path is None:
            environment_path = RCManager.get_environment_manager_path(logfile=log)

        cls._install_nb_strip_out(environment_path)
        cls._activate_nb_strip_out(environment_path, location)

    @classmethod
    def teardown(cls, location, environment_path=None):

        log = location / GRYPHON_RC
        if environment_path is None:
            environment_path = RCManager.get_environment_manager_path(logfile=log)

        cls._deactivate_nb_strip_out(environment_path, location)
        cls._uninstall_nb_strip_out(environment_path)
