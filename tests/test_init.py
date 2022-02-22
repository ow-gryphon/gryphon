from gryphon.core.init import init
from gryphon.core.registry import Template
from .utils import TEST_FOLDER


def test_init_1(setup, teardown):
    cwd = setup()
    project = cwd / "project"

    try:

        template = Template.template_from_path(TEST_FOLDER / "data" / "analytics")
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
