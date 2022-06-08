import time
import zipfile
from os.path import normpath, basename
from pathlib import Path
from typing import List

import yaml

from .core_text import Text
from .operations import RCManager
from ..constants import SUCCESS
from ..logger import logger


def get_output_file_name(path):
    timestamp = time.strftime("%Y%m%d_%Hh%Mm%Ss", time.localtime())
    project_name = basename(normpath(path))
    return path.parent / f"{project_name}_handover_{timestamp}.zip"


def write_log_file(excluded_large_files, excluded_gryphon_files, output_file_name, handover_settings):
    data = dict(
        excluded_large_files=excluded_large_files,
        excluded_gryphon_files=excluded_gryphon_files,
        **handover_settings
    )
    with open(str(output_file_name)[:-4] + "_log.txt", "w") as f:
        yaml.dump(data, f)


def handover(
    path: Path,
    output_path: Path,
    gryphon_exclusion_list: List[str],
    large_files_exclusion_list: List[str],
    file_list: List[str],
    configs: dict
):
    logger.info("Creating zip package.")

    with zipfile.ZipFile(output_path, mode="w") as zip_file:
        for f in file_list:
            if f not in gryphon_exclusion_list and f not in large_files_exclusion_list:
                zip_file.write(filename=path / f)

    logfile = RCManager.get_rc_file(path)
    RCManager.get_environment_manager_path(logfile)
    # TODO: call pip freeze and log the installed libs

    write_log_file(large_files_exclusion_list, gryphon_exclusion_list, output_path, configs)
    logger.log(SUCCESS, f"{Text.handover_end_message} {output_path}")
