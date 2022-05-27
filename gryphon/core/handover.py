import zipfile
import time
from pathlib import Path
from typing import List
from ..logger import logger
from ..constants import SUCCESS


def handover(path: Path, exclusion_list: List[str], file_list: List[str]):
    logger.info("Creating zip package.")
    timestamp = time.strftime("%Y_%m_%d_%H_%M_%S", time.gmtime())
    file = Path.cwd() / f"handover_{timestamp}.zip"

    with zipfile.ZipFile(file, mode="w") as zip_file:
        for f in file_list:
            if f not in exclusion_list:
                zip_file.write(filename=path / f)

    logger.log(SUCCESS, f"Handover package successfully generated: {file}")

# TODO: use prefix to the file name with the project name
# TODO: have a file limit on .gryphon_rc

# TODO: keep
# TODO: Ask the user if he wants to keep gryphon generated files on the zip (template ones)
