import platform

from ...fsm import State, Transition
from ...logger import logger
from ...wizard.functions import erase_lines
from ...wizard.questions import InitFromExistingQuestions


class AskExternalEnvPath(State):
    name = "ask_external_env_path"
    transitions = [
        Transition(
            next_state="ask_project_info",
            condition=lambda context: True
        )
    ]

    @staticmethod
    def handle_not_environment(context, path):
        erase_lines(n_lines=1)
        erase_lines(n_lines=context["extra_lines"])
        logger.warning(f"External environment not found in the provided folder {path}. Try again.\n")
        erase_lines(n_lines=1)
        context["extra_lines"] = 1

    def on_start(self, context: dict) -> dict:
        context["extra_lines"] = 0

        while True:
            path = InitFromExistingQuestions.ask_external_env_path()
            if path.is_dir():
                if platform.system() == "Windows":
                    # On Windows the venv folder structure is different from unix
                    pip_path = path / "Scripts" / "pip.exe"
                else:
                    pip_path = path / "bin" / "pip"

                if pip_path.is_file():
                    break
                elif (path / "conda-meta").is_dir():
                    break
                else:
                    self.handle_not_environment(context, path)

            else:
                self.handle_not_environment(context, path)

        context["external_env_path"] = path
        return context
