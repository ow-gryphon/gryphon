import time
import zipfile
from os.path import normpath, basename
from pathlib import Path
from typing import List

from ..constants import SUCCESS
from ..logger import logger


def handover(path: Path, exclusion_list: List[str], file_list: List[str]):
    logger.info("Creating zip package.")

    timestamp = time.strftime("%Y_%m_%d_%H_%M_%S", time.gmtime())
    project_name = basename(normpath(path))

    file = Path.cwd() / f"{project_name}_handover_{timestamp}.zip"

    with zipfile.ZipFile(file, mode="w") as zip_file:
        for f in file_list:
            if f not in exclusion_list:
                zip_file.write(filename=path / f)

    logger.log(SUCCESS, f"Handover package successfully generated: {file}")

# DONE: use prefix to the file name with the project name
# TODO: have a file limit on .gryphon_rc
# TODO: Ask the user if he wants to keep gryphon generated files on the zip (template ones)
# DONE: Keep list of files created by gryphon on .gryphon_rc
# TODO: Think about freeze feature (at time of handover)
