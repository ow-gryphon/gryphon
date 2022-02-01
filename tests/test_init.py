import json
from gryphon.core.init import init
from .utils import TEST_FOLDER


def test_init_1(setup, teardown):
    cwd = setup()
    project = cwd / "project"

    try:
        init(
            template_path=TEST_FOLDER / "data" / "analytics",
            location=project
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


def test_create_conda_env_3(setup, teardown, mocker):
    """
    Test case:
    A venv is created in a folder that does not exists previously.
    """
    read_data = json.dumps({
        "environment_management": "placeholder"
    })

    mock_open = mocker.mock_open(read_data=read_data)
    with mocker.patch("__main__.open", mock_open):

        cwd = setup()
        try:
            # with pytest.raises(Exception):
            init(
                template_path=TEST_FOLDER / "data" / "analytics",
                location=cwd
            )
        except:
            raise ValueError()

        finally:
            teardown()
