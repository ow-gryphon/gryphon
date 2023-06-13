import logging
import os
import platform
from pathlib import Path

from .bash_utils import BashUtils
from ...constants import VENV_FOLDER, CONDA, VENV


REQUIREMENTS = "requirements.txt"
REQUIREMENTS_NOT_FOUND = "requirements.txt file not found."


logger = logging.getLogger('gryphon')


class NBExtensionsManager:

    @staticmethod
    def _remove_from_requirements(requirements_path: Path):

        if not requirements_path.is_file():
            raise FileNotFoundError(REQUIREMENTS_NOT_FOUND)

        with open(requirements_path, "r", encoding="UTF-8") as f1:
            lines = f1.readlines()

        libs_to_remove = ["jupyter_nbextensions_configurator", "jupyter_contrib_nbextensions"]
        lines = list(filter(lambda lib: lib not in libs_to_remove, lines))

        with open(requirements_path, "w", encoding="UTF-8") as f2:
            f2.writelines(lines)

    @classmethod
    def install(cls, environment_manager, environment_path):
        if environment_manager == VENV:
            cls.install_extra_nbextensions_venv(environment_path=environment_path)
        elif environment_manager == CONDA:
            cls.install_extra_nbextensions_conda(environment_path=environment_path)

    @classmethod
    def teardown(cls, environment_manager, environment_path):

        if environment_manager == VENV:
            cls.uninstall_extra_nbextensions_venv(environment_path=environment_path)
        elif environment_manager == CONDA:
            cls.uninstall_extra_nbextensions_conda(environment_path=environment_path)

    @staticmethod
    def install_extra_nbextensions_conda(environment_path=None, requirements_path=None):
        """
        Function to install the libraries from a 'requirements.txt' file
        """

        if requirements_path is None:
            assert environment_path is not None
            requirements_path = environment_path.parent / REQUIREMENTS

        if not environment_path.is_dir():
            raise RuntimeError(f"Conda environment not found inside folder. Should be at {environment_path}"
                               f"\nAre you using conda instead of venv?")

        if not requirements_path.is_file():
            raise FileNotFoundError(REQUIREMENTS_NOT_FOUND)

        with open(requirements_path, "r", encoding="UTF-8") as f1:
            requirements = f1.read()

        for lib in ["jupyter_nbextensions_configurator", "jupyter_contrib_nbextensions"]:
            if lib not in requirements:
                with open(requirements_path, "a", encoding="UTF-8") as f2:
                    f2.write(f"\n{lib}")

        if platform.system() == "Windows":
            # On Windows the venv folder structure is different from unix
            conda_python = environment_path / "python.exe"
            conda_pip = environment_path / "Scripts" / "pip"
            silent = "START /B \"\""
            redirect = ">nul 2>&1"
        else:
            conda_python = environment_path / "bin" / "python"
            conda_pip = environment_path / "bin" / "pip"
            silent = "nohup"
            redirect = ""

        return_code, _ = BashUtils.execute_and_log(
            f'\"{conda_pip}\" install jupyter_contrib_nbextensions '
            f'jupyter_nbextensions_configurator  --disable-pip-version-check '
            f'--no-warn-script-location'
            # --prefix=\"{environment_path}\" --yes -k'
        )

        if return_code is not None:
            raise RuntimeError(f"Failed on conda install command. Return code: {return_code}")

        try:
            return_code, _ = BashUtils.execute_and_log(
                f'({silent} \"{conda_python}\" -m jupyter nbextensions_configurator enable --user) {redirect}')
            assert return_code is None

            return_code, _ = BashUtils.execute_and_log(
                f'({silent} \"{conda_python}\" -m jupyter nbextension enable codefolding/main --user) {redirect}')
            assert return_code is None

            return_code, _ = BashUtils.execute_and_log(
                f'({silent} \"{conda_python}\" -m jupyter contrib nbextension install --user) {redirect}')
            assert return_code is None

            return_code, _ = BashUtils.execute_and_log(
                f'({silent} \"{conda_python}\" -m jupyter nbextension enable toc2/main --user) {redirect}')
            assert return_code is None

            return_code, _ = BashUtils.execute_and_log(
                f'({silent} \"{conda_python}\" -m '
                f'jupyter nbextension enable collapsible_headings/main --user) {redirect}'
            )
            assert return_code is None

        except AssertionError:
            raise RuntimeError(f"Failed to install jupyter nbextensions. Return code: {return_code}")

    @staticmethod
    def install_extra_nbextensions_venv(requirements_path=None, environment_path=None):
        """
        Function to install the libraries from a 'requirements.txt' file
        """
        target_folder = Path.cwd()

        if environment_path is None:
            venv_folder = target_folder / VENV_FOLDER
        else:
            venv_folder = environment_path

        if requirements_path is None:
            requirements_path = target_folder / REQUIREMENTS

        if platform.system() == "Windows":
            # On Windows the venv folder structure is different from unix
            pip_path = venv_folder / "Scripts" / "pip.exe"
            activate_env_command = venv_folder / "Scripts" / "activate.bat"
            silent = "START /B \"\""
            redirect = ">nul 2>&1"
        else:
            pip_path = venv_folder / "bin" / "pip"
            # Some Python installations on Unix systems only have access to pip3
            if not pip_path.is_file():
                pip_path = venv_folder / "bin" / "pip3"
            activate_path = venv_folder / "bin" / "activate"
            activate_env_command = str(activate_path)
            os.system(f"chmod 777 \"{activate_path}\"")
            silent = "nohup"
            redirect = ""

        # Install requirements
        if not pip_path.is_file():
            raise RuntimeError(f"Virtual environment not found inside folder. Should be at {pip_path}"
                               f"\nAre you using venv instead of conda?")

        if not requirements_path.is_file():
            raise FileNotFoundError(REQUIREMENTS_NOT_FOUND)

        with open(requirements_path, "r", encoding="UTF-8") as f1:
            requirements = f1.read()

        for lib in ["jupyter_nbextensions_configurator", "jupyter_contrib_nbextensions"]:
            if lib not in requirements:
                with open(requirements_path, "a", encoding="UTF-8") as f2:
                    f2.write(f"\n{lib}")

        return_code, _ = BashUtils.execute_and_log(
            f'\"{activate_env_command}\" && pip --disable-pip-version-check install '
            f'jupyter_contrib_nbextensions jupyter_nbextensions_configurator'
        )

        # On some Python installations on Unix systems, only pip3 is available
        if return_code == 32512:
            return_code, _ = BashUtils.execute_and_log(
                f'\"{activate_env_command}\" && pip3 --disable-pip-version-check install '
                f'jupyter_contrib_nbextensions jupyter_nbextensions_configurator'
            )

        if return_code is not None:
            raise RuntimeError(f"Failed on pip install command. Return code: {return_code}")

        # os.chdir(target_folder)
        return_code, _ = BashUtils.execute_and_log(
            f"\"{activate_env_command}\" "
            f"&& ({silent} jupyter nbextensions_configurator enable --user) {redirect}"
            f"&& ({silent} jupyter contrib nbextension install --user) {redirect}"
            f"&& ({silent} jupyter nbextension enable codefolding/main --user) {redirect}"
            f"&& ({silent} jupyter nbextension enable toc2/main --user) {redirect}"
            f"&& ({silent} jupyter nbextension enable collapsible_headings/main --user) {redirect}"
        )

        if return_code is not None:
            raise RuntimeError(f"Failed to install jupyter nbextensions. Return code: {return_code}")

    @classmethod
    def uninstall_extra_nbextensions_conda(cls, environment_path=None, requirements_path=None):
        """
        Function to install the libraries from a 'requirements.txt' file
        """

        # Install requirements
        logger.info("Uninstalling extra notebook extensions.")
        if requirements_path is None:
            assert environment_path is not None
            requirements_path = environment_path.parent / REQUIREMENTS

        if not environment_path.is_dir():
            raise RuntimeError(f"Conda environment not found inside folder. Should be at {environment_path}"
                               f"\nAre you using conda instead of venv?")

        cls._remove_from_requirements(requirements_path)

        if platform.system() == "Windows":
            # On Windows the venv folder structure is different from unix
            conda_python = environment_path / "python.exe"
            conda_pip = environment_path / "Scripts" / "pip"
            silent = "START /B \"\""
            redirect = ">nul 2>&1"
        else:
            conda_python = environment_path / "bin" / "python"
            conda_pip = environment_path / "bin" / "pip"
            silent = "nohup"
            redirect = ""

        return_code, _ = BashUtils.execute_and_log(
            f'\"{conda_pip}\" uninstall jupyter_contrib_nbextensions jupyter_nbextensions_configurator -y'
            # --prefix=\"{environment_path}\" --yes -k'
        )

        if return_code is not None:
            raise RuntimeError(f"Failed on conda install command. Return code: {return_code}")

        try:
            return_code, _ = BashUtils.execute_and_log(
                f'({silent} \"{conda_python}\" -m jupyter nbextensions_configurator disable --user) {redirect}')
            assert return_code is None

            return_code, _ = BashUtils.execute_and_log(
                f'({silent} \"{conda_python}\" -m jupyter nbextension disable codefolding/main --user) {redirect}')
            assert return_code is None

            return_code, _ = BashUtils.execute_and_log(
                f'({silent} \"{conda_python}\" -m jupyter nbextension disable toc2/main --user) {redirect}')
            assert return_code is None

            return_code, _ = BashUtils.execute_and_log(
                f'({silent} \"{conda_python}\" -m '
                f'jupyter nbextension disable collapsible_headings/main --user) {redirect}'
            )
            assert return_code is None

            return_code, _ = BashUtils.execute_and_log(
                f'({silent} \"{conda_python}\" -m jupyter contrib nbextension uninstall --user) {redirect}')
            assert return_code is None

        except AssertionError:
            raise RuntimeError(f"Failed to uninstall jupyter nbextensions. Return code: {return_code}")

    @classmethod
    def uninstall_extra_nbextensions_venv(cls, requirements_path=None, environment_path=None):
        """
        Function to install the libraries from a 'requirements.txt' file
        """
        target_folder = Path.cwd()

        if environment_path is None:
            venv_folder = target_folder / VENV_FOLDER
        else:
            venv_folder = environment_path

        if requirements_path is None:
            requirements_path = target_folder / REQUIREMENTS

        if platform.system() == "Windows":
            # On Windows the venv folder structure is different from unix
            pip_path = venv_folder / "Scripts" / "pip.exe"
            activate_env_command = venv_folder / "Scripts" / "activate.bat"
            silent = "START /B \"\""
            redirect = ">nul 2>&1"
        else:
            pip_path = venv_folder / "bin" / "pip"
            # On some installations on Unix systems, only pip3 is available
            if not pip_path.is_file():
                pip_path = venv_folder / "bin" / "pip3"
            activate_path = venv_folder / "bin" / "activate"
            activate_env_command = str(activate_path)
            os.system(f"chmod 777 \"{activate_path}\"")
            silent = "nohup"
            redirect = ""

        # Install requirements
        logger.info("Uninstalling notebook extensions.")

        if not pip_path.is_file():
            raise RuntimeError(f"Virtual environment not found inside folder. Should be at {pip_path}"
                               f"\nAre you using venv instead of conda?")

        cls._remove_from_requirements(requirements_path)

        return_code, _ = BashUtils.execute_and_log(
            f"\"{activate_env_command}\" "
            f"&& ({silent} jupyter nbextension disable codefolding/main --user) {redirect}"
            f"&& ({silent} jupyter nbextension disable toc2/main --user) {redirect}"
            f"&& ({silent} jupyter nbextension disable collapsible_headings/main --user) {redirect}"
            f"&& ({silent} jupyter nbextensions_configurator disable --user) {redirect}"
            f"&& ({silent} jupyter contrib nbextension uninstall --user) {redirect}"
        )

        return_code, _ = BashUtils.execute_and_log(
            f'\"{activate_env_command}\" && pip --disable-pip-version-check uninstall '
            f'jupyter_contrib_nbextensions jupyter_nbextensions_configurator -y'
        )

        # On some installations on Unix systems, only pip3 is available
        if return_code == 32512:
            return_code, _ = BashUtils.execute_and_log(
                f'\"{activate_env_command}\" && pip3 --disable-pip-version-check uninstall '
                f'jupyter_contrib_nbextensions jupyter_nbextensions_configurator -y'
            )

        if return_code is not None:
            raise RuntimeError(f"Failed on pip uninstall command. Return code: {return_code}")

        if return_code is not None:
            raise RuntimeError(f"Failed to install jupyter nbextensions. Return code: {return_code}")
