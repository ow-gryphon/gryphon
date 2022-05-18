import logging
import os
import platform
import sys
from pathlib import Path

from .bash_utils import BashUtils
from .path_utils import PathUtils
from ..core_text import Text
from ...constants import (
    SUCCESS, VENV_FOLDER, CONDA_FOLDER, ALWAYS_ASK, GRYPHON_HOME,
    SYSTEM_DEFAULT
)

logger = logging.getLogger('gryphon')


REQUIREMENTS = "requirements.txt"
REQUIREMENTS_NOT_FOUND = "requirements.txt file not found."


class EnvironmentManagerOperations:

    # VENV
    @classmethod
    def create_venv(cls, folder=None, python_version=None):
        """Function to a virtual environment inside a folder."""
        python_path = "python"
        if python_version and python_version not in [ALWAYS_ASK, SYSTEM_DEFAULT]:

            env_folder = GRYPHON_HOME / f"reserved_env_python_{python_version}"
            if not env_folder.is_dir():
                logger.info(f"Installing python version with Conda.")
                cls.create_conda_env(
                    folder=GRYPHON_HOME / f"reserved_env_python_{python_version}",
                    python_version=python_version
                )

            if platform.system() == "Windows":
                # On Windows the venv folder structure is different from unix
                python_path = env_folder / CONDA_FOLDER / "python.exe"
            else:
                python_path = env_folder / CONDA_FOLDER / "bin" / "python"

        venv_path = target_folder = PathUtils.get_destination_path(folder)
        # venv_path = target_folder / VENV_FOLDER

        # Create venv
        logger.info(f"Creating virtual environment in {venv_path}")
        return_code, _ = BashUtils.execute_and_log(f"\"{python_path}\" -m venv \"{venv_path}\"")
        if return_code:
            raise RuntimeError("Failed to create virtual environment.")

        logger.log(SUCCESS, "Done creating virtual environment.")

        return venv_path

    @staticmethod
    def install_libraries_venv(requirements_path=None, environment_path=None):
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
        else:
            pip_path = venv_folder / "bin" / "pip"

        # Install requirements
        logger.info("Installing requirements. This may take several minutes ...")

        if not pip_path.is_file():
            raise RuntimeError(f"Virtual environment not found inside folder. Should be at {pip_path}."
                               f"\nAre you using venv instead of conda?")

        if not requirements_path.is_file():
            raise FileNotFoundError(REQUIREMENTS_NOT_FOUND)

        return_code, output = BashUtils.execute_and_log(
            f'\"{pip_path}\" install -r \"{requirements_path}\"'
            f' --disable-pip-version-check'
        )

        if return_code is not None:
            # TODO: take the error output from stderr
            if "Could not find a version that satisfies the requirement" in output:
                logger.error(output)
            else:
                logger.error(f"Failed on pip install command. Status code: {return_code}")
        else:
            logger.log(SUCCESS, "Installation successful!")

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

    @staticmethod
    def change_shell_folder_and_activate_venv(location, alternative_env=None):

        target_folder = PathUtils.get_destination_path(location)
        if alternative_env:
            env_folder = alternative_env
        else:
            env_folder = target_folder / VENV_FOLDER

        if platform == "windows":
            logger.warning(f"""
                {Text.install_end_message_1}
    
                ANACONDA PROMPT/COMMAND PROMPT:
    
                >> cd \"{target_folder}\"
                >> {env_folder / "Scripts" / "activate.bat"}
    
                GIT BASH:
    
                >> cd \"{str(target_folder).replace(chr(92), '/')}\"
                >> source {env_folder / "Scripts" / "activate"}
    
                {Text.install_end_message_2}
            """)
        else:
            logger.warning(f"""
                {Text.install_end_message_1}

                >> cd \"{str(target_folder).replace(chr(92), '/')}\"
                >> source {env_folder / "scripts" / "activate"}

                {Text.install_end_message_2}
            """)

    # CONDA
    @staticmethod
    def create_conda_env(folder=None, python_version=None):
        """Function to a virtual environment inside a folder."""
        conda_path = target_folder = PathUtils.get_destination_path(folder)
        # conda_path = target_folder / CONDA_FOLDER

        # Create venv
        logger.info(f"Creating Conda virtual environment in {conda_path}")
        BashUtils.execute_and_log("conda config --append channels conda-forge --json >> out.json")
        if Path("out.json").is_file():
            os.remove("out.json")

        command = f"conda create --prefix=\"{conda_path}\" -y -k"

        if python_version and python_version != SYSTEM_DEFAULT and python_version != ALWAYS_ASK:
            command += f" python={python_version}"

        return_code, _ = BashUtils.execute_and_log(command)
        if return_code is not None:
            raise RuntimeError(f"Failed to create conda environment. Status code: {return_code}")

        logger.log(SUCCESS, "Done creating virtual environment.")
        return conda_path

    @staticmethod
    def install_libraries_conda(environment_path=None, requirements_path=None):
        """
            TODO:  Mensagem achada quando pedimos uma versão que nao existe usando conda
            PackagesNotFoundError: The following packages are not available from current channels:

              - matplotlib==1.5.8

            Current channels:

              - https://repo.anaconda.com/pkgs/main/linux-64
              - https://repo.anaconda.com/pkgs/main/noarch
              - https://repo.anaconda.com/pkgs/r/linux-64
              - https://repo.anaconda.com/pkgs/r/noarch
              - https://conda.anaconda.org/conda-forge/linux-64
              - https://conda.anaconda.org/conda-forge/noarch

            To search for alternate channels that may provide the conda package you're
            looking for, navigate to
        """
        logger.info("Installing requirements. This may take several minutes ...")

        target_folder = Path.cwd()

        if environment_path is None:
            conda_path = target_folder / VENV_FOLDER
        else:
            conda_path = environment_path

        if requirements_path is None:
            requirements_path = target_folder / REQUIREMENTS

        if not conda_path.is_dir():
            raise RuntimeError(f"Conda environment not found inside folder. Should be at {conda_path}"
                               f"\nAre you using conda instead of venv?")

        return_code, output = BashUtils.execute_and_log(
            f"conda install --prefix \"{conda_path}\""
            f" --file \"{requirements_path}\" -k -y"
        )

        if return_code is not None:
            # TODO: take the error output from stderr
            if "Could not find a version that satisfies the requirement" in output:
                logger.error(output)
            else:
                logger.error(f"Failed on pip install command. Status code: {return_code}")
        else:
            logger.log(SUCCESS, "Installation successful!")

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
            silent = "START /B \"\""
            redirect = ">nul 2>&1"
        else:
            conda_python = environment_path / "bin" / "python"
            silent = "nohup"
            redirect = ""

        return_code, _ = BashUtils.execute_and_log(
            f'conda install jupyter_contrib_nbextensions '
            f'jupyter_nbextensions_configurator --prefix=\"{environment_path}\" --yes -k'
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
    def change_shell_folder_and_activate_conda_env(location, alternative_env=None):
        target_folder = PathUtils.get_destination_path(location)

        if alternative_env:
            env_folder = alternative_env
        else:
            env_folder = target_folder / CONDA_FOLDER

        logger.warning(f"""
            {Text.install_end_message_1}

            >> cd {target_folder}
            >> conda activate --prefix=\"{env_folder}\"

            {Text.install_end_message_2}
        """)

    @staticmethod
    def update_conda():
        if BashUtils.execute_and_log("conda update conda -k -y")[0] is not None:
            raise RuntimeError("Failed to update conda.")
