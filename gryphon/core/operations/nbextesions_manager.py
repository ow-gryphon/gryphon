import logging
import os
import platform
from pathlib import Path

from .bash_utils import BashUtils
from ...constants import VENV_FOLDER


REQUIREMENTS = "requirements.txt"
REQUIREMENTS_NOT_FOUND = "requirements.txt file not found."


logger = logging.getLogger('gryphon')


class NBExtensionsManager:

    @staticmethod
    def install_extra_nbextensions_conda(environment_path=None, requirements_path=None):
        """
        Function to install the libraries from a 'requirements.txt' file
        """

        # Install requirements
        logger.info("Installing extra notebook extensions.")

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
            f'jupyter_nbextensions_configurator'  # --prefix=\"{environment_path}\" --yes -k'
        )

        if return_code is not None:
            raise RuntimeError(f"Failed on conda install command. Return code: {return_code}")

        # os.chdir(target_folder)

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
            # os.remove("nohup.out")

        except AssertionError:
            raise RuntimeError(f"Failed to install jupyter nbextensions. Return code: {return_code}")

        # os.chdir(target_folder.parent)

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
            activate_path = venv_folder / "bin" / "activate"
            activate_env_command = str(activate_path)
            os.system(f"chmod 777 \"{activate_path}\"")
            silent = "nohup"
            redirect = ""

        # Install requirements
        logger.info("Installing extra notebook extensions.")

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

        # os.chdir(target_folder.parent)
