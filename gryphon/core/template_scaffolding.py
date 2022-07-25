import logging
from pathlib import Path

from .common_operations import (
    init_new_git_repo, initial_git_commit,
)
from .operations import (BashUtils, SettingsManager)
from ..constants import (DATA_PATH, SUCCESS)

logger = logging.getLogger('gryphon')


def template_scaffolding(location: Path):

    template_path = DATA_PATH / "template_scaffolding"
    location = Path(location)

    logger.info("Creating project scaffolding.")
    logger.info(f"Initializing project at {location}")

    # Files
    BashUtils.copy_project_template(
        template_destiny=location,
        template_source=Path(template_path)
    )

    # TODO: JOIN ALL THE requirements.txt files in one at the time of project
    #  init with more than one zip file downloaded.

    # Git
    repo = init_new_git_repo(folder=location)
    initial_git_commit(repo)

    # install pre-commit hooks

    SettingsManager.add_local_template(str(Path(location).absolute()))
    logger.info("Added new template into the gryphon registry. You will be able to find it inside gryphon according"
                " to the information given on metadata.json file.\n\n In order to find it on gryphon menus you will"
                " have to fill the template information inside metadata.json file (providing at least the display "
                "name and the command).")
    logger.log(SUCCESS, "Installation successful!")

# TODO: prompt whether the template scaffolding is for init or generate]
# TODO: way to choose which pre-commit hooks ones want to add
