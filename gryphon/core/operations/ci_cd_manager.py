import shutil
from pathlib import Path

from ...constants import DATA_PATH


class CICDManager:

    @staticmethod
    def setup_ci_cd(location: Path):
        ci_cd_folder = DATA_PATH / "ci_cd"  # / ".github"
        # shutil.copytree(
        #     src=ci_cd_folder,
        #     dst=location
        # )
