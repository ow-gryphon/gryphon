import shutil
from gryphon.core.init import init
from gryphon.core.registry import Template
from .utils import TEST_FOLDER, CONFIG_FILE_NAME, MOCK_CONFIG_FILE_PATH


def test_init_1(setup, teardown, mocker):
    cwd = setup()
    project = cwd / "project"
    file = cwd / CONFIG_FILE_NAME
    shutil.copy(
        src=TEST_FOLDER / "data" / "gryphon_config_venv.json",
        dst=file
    )

    with mocker.patch(
        target=MOCK_CONFIG_FILE_PATH,
        return_value=file
    ):

        try:

            template = Template.template_from_path(TEST_FOLDER / "data" / "analytics", type="local")
            init(
                template=template,
                location=project,
                python_version="3.7"
            )
            scr_path = project / "src"
            notebooks_path = project / "notebooks"
            venv_path = project / ".venv"
            requirements_path = project / "requirements.txt"
            gitignore_path = project / ".gitignore"

            assert scr_path.is_dir()
            assert notebooks_path.is_dir()
            assert venv_path.is_dir()

            assert requirements_path.is_file()
            assert gitignore_path.is_file()

        finally:
            teardown()
