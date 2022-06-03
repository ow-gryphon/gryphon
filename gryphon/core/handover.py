import time
import zipfile
from os.path import normpath, basename
from pathlib import Path
from typing import List

from ..constants import SUCCESS
from ..logger import logger


def get_output_file_name(path):
    timestamp = time.strftime("%Y%m%d_%H%M%S", time.gmtime())
    project_name = basename(normpath(path))
    return path.parent / f"{project_name}_handover_{timestamp}.zip"


def handover(path: Path, output_path: Path, exclusion_list: List[str], file_list: List[str]):
    logger.info("Creating zip package.")

    with zipfile.ZipFile(output_path, mode="w") as zip_file:
        for f in file_list:
            if f not in exclusion_list:
                zip_file.write(filename=path / f)

    logger.log(SUCCESS, f"Handover package successfully generated: {output_path}")

# DONE: use prefix to the file name with the project name
# DONE: have a file limit on .gryphon_rc
# DONE: Ask the user if he wants to keep gryphon generated files on the zip (template ones)
# DONE: Keep list of files created by gryphon on .gryphon_rc
# TODO: Think about freeze feature (at time of handover)
