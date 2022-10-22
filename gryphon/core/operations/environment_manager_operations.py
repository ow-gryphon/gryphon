import logging
import os
import platform
from pathlib import Path

from .bash_utils import BashUtils
from .path_utils import PathUtils
from ..core_text import Text
from ...constants import (
    SUCCESS, VENV_FOLDER, CONDA_FOLDER, ALWAYS_ASK, GRYPHON_HOME,
    SYSTEM_DEFAULT, CONDA, VENV
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

        venv_path = PathUtils.get_destination_path(folder)

        # Create venv
        logger.info(f"Creating virtual environment in {venv_path}")
        return_code, _ = BashUtils.execute_and_log(f"\"{python_path}\" -m venv \"{venv_path}\"")
        if return_code:
            raise RuntimeError("Failed to create virtual environment.")
            # TODO: Check whats happened

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

    # CONDA
    @staticmethod
    def create_conda_env(folder=None, python_version=None):
        """Function to a virtual environment inside a folder."""
        conda_path = PathUtils.get_destination_path(folder)

        # Create venv
        logger.info(f"Creating Conda virtual environment in {conda_path}")
        BashUtils.execute_and_log("conda config --append channels conda-forge --json >> out.json")
        if Path("out.json").is_file():
            os.remove("out.json")

        command = f"conda create --prefix=\"{conda_path}\""

        if python_version and python_version != SYSTEM_DEFAULT and python_version != ALWAYS_ASK:
            command += f" python={python_version}"

        command += " pip -y -k"

        return_code, _ = BashUtils.execute_and_log(command)
        if return_code is not None:
            raise RuntimeError(f"Failed to create conda environment. Status code: {return_code}")

        BashUtils.execute_and_log("conda config --append channels conda-forge --json >> out.json")

        logger.log(SUCCESS, "Done creating virtual environment.")
        return conda_path

    @staticmethod
    def install_libraries_conda(environment_path=None, requirements_path=None):
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

        # return_code, output = BashUtils.execute_and_log(
        #     f"conda install --prefix \"{conda_path}\""
        #     f" --file \"{requirements_path}\" -k -y"
        # )

        if platform.system() == "Windows":
            # On Windows the venv folder structure is different from unix
            conda_pip = environment_path / "Scripts" / "pip"
        else:
            conda_pip = environment_path / "bin" / "pip"

        return_code, output = BashUtils.execute_and_log(
            f"\"{conda_pip}\" install -r \"{requirements_path}\""
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
    def update_conda():
        if BashUtils.execute_and_log("conda update conda -k -y")[0] is not None:
            raise RuntimeError("Failed to update conda.")

    @staticmethod
    def final_instructions(location, env_manager, alternative_env=None):
        target_folder = PathUtils.get_destination_path(location)
        env_folder = alternative_env

        if env_manager == CONDA:

            if not alternative_env:
                env_folder = target_folder / CONDA_FOLDER

            logger.warning(f"""
                    {Text.install_end_message_1}

                        >> cd \"{target_folder.relative_to(Path.cwd())}\"
                        >> conda activate --prefix=\"{env_folder.relative_to(target_folder)}\"

                        {Text.install_end_message_2}
                    """)

        elif env_manager == VENV:

            if not alternative_env:
                env_folder = target_folder / VENV_FOLDER

            if platform.system() == "Windows":

                logger.warning(f"""
                {Text.install_end_message_1}

                    ANACONDA PROMPT/COMMAND PROMPT:

                    >> cd \"{target_folder.relative_to(Path.cwd())}\"
                    >> {(env_folder / "Scripts" / "activate").relative_to(target_folder)}

                    GIT BASH:

                    >> cd \"{str(target_folder).replace(chr(92), '/')}\"
                    >> source {(env_folder / "Scripts" / "activate").relative_to(target_folder)}

                {Text.install_end_message_2}
                """)
            else:

                logger.warning(f"""
                {Text.install_end_message_1}

                    >> cd \"{str(target_folder.relative_to(Path.cwd())).replace(chr(92), '/')}\"
                    >> source {(env_folder / "scripts" / "activate").relative_to(target_folder)}

                {Text.install_end_message_2}
                """)
