import time
import zipfile
from os.path import normpath, basename
from pathlib import Path
from typing import List

import yaml

from .operations import RCManager
from ..constants import SUCCESS
from ..logger import logger


def get_output_file_name(path):
    timestamp = time.strftime("%Y%m%d_%H%M%S", time.gmtime())
    project_name = basename(normpath(path))
    return path.parent / f"{project_name}_handover_{timestamp}.zip"


def write_log_file(excluded_large_files, excluded_gryphon_files, output_file_name, handover_settings):
    data = dict(
        excluded_large_files=excluded_large_files,
        excluded_gryphon_files=excluded_gryphon_files,
        **handover_settings
    )
    with open(str(output_file_name)[:-4] + ".txt", "w") as f:
        yaml.dump(data, f)


def handover(path: Path, output_path: Path, gryphon_exclusion_list: List[str],
             large_files_exclusion_list: List[str], file_list: List[str], configs: dict):
    logger.info("Creating zip package.")

    with zipfile.ZipFile(output_path, mode="w") as zip_file:
        for f in file_list:
            if f not in gryphon_exclusion_list and f not in large_files_exclusion_list:
                zip_file.write(filename=path / f)

    logfile = RCManager.get_rc_file(path)
    env_manager_path = RCManager.get_environment_manager_path(logfile)

    write_log_file(large_files_exclusion_list, gryphon_exclusion_list, output_path, configs)
    logger.log(SUCCESS, f"Handover package successfully generated: {output_path}")

# DONE: use prefix to the file name with the project name
# DONE: have a file limit on .gryphon_rc
# DONE: Ask the user if he wants to keep gryphon generated files on the zip (template ones)
# DONE: Keep list of files created by gryphon on .gryphon_rc
# TODO: Think about freeze feature (at time of handover)
