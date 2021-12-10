import os
import pytest
import pexpect

KEY_UP = '\x1b[A'
KEY_DOWN = '\x1b[B'
KEY_RIGHT = '\x1b[C'
KEY_LEFT = '\x1b[D'


def test_cli_1(setup, teardown, get_pip_libraries):

    file_name = "segmentation"
    project_folder = "project"
    lib_name = "scipy"

    cwd = setup()
    try:
        os.system(f"labskit init analytics_git {project_folder}")
        os.chdir(project_folder)
        os.system(f"labskit generate mlclustering_git {file_name}")
        os.system(f"labskit add {lib_name}")

        assert (cwd / project_folder).is_dir()
        assert (cwd / project_folder / "src").is_dir()
        assert (cwd / project_folder / "notebooks").is_dir()
        assert (cwd / project_folder / "tests").is_dir()
        assert (cwd / project_folder / "src" / f"clustering_{file_name}.py").is_file()
        assert lib_name in get_pip_libraries(cwd / project_folder)
    except Exception as e:
        pytest.fail("Raised exception", e)
    finally:
        teardown()


def wizard_init(project_folder):
    child = pexpect.spawn('python', ['../lkit.py'])
    child.expect('Welcome to Griffin')
    child.sendcontrol('m')
    child.expect('basic')
    child.send(KEY_DOWN)
    child.sendcontrol('m')
    child.expect('Path to render the template')
    child.send(project_folder)
    child.sendcontrol('m')
    child.expect('Confirm that you want')
    child.sendcontrol('m')
    child.expect('Installation succeeded')
    child.close()


def wizard_generate(file_name):
    child = pexpect.spawn('python', ['../../lkit.py'])
    child.expect('Welcome to Griffin')
    child.send(KEY_DOWN)
    child.sendcontrol('m')
    child.expect('mlclustering_git')
    child.sendcontrol('m')
    child.expect('Name of the file')
    child.send(file_name)
    child.sendcontrol('m')
    child.expect('Confirm that you want')
    child.sendcontrol('m')
    child.expect('Installation succeeded')
    child.close()


def wizard_add(lib_name):
    child = pexpect.spawn('python', ['../../lkit.py'])
    child.expect('Welcome to Griffin')
    child.send(KEY_DOWN * 2)
    child.sendcontrol('m')
    child.expect('data visualization')
    child.send(KEY_DOWN * 5)
    child.sendcontrol('m')
    child.expect('Type the python library')
    child.send(lib_name)
    child.sendcontrol('m')
    child.expect('Confirm that you want')
    child.sendcontrol('m')
    child.expect('Installation succeeded')
    child.close()


def test_wizard_1(setup, teardown, get_pip_libraries):

    file_name = "segmentation"
    project_folder = "project"
    lib_name = "scipy"

    cwd = setup()
    try:
        wizard_init(project_folder)
        os.chdir(project_folder)
        wizard_generate(file_name)
        wizard_add(lib_name)

        assert (cwd / project_folder).is_dir()
        assert (cwd / project_folder / "src").is_dir()
        assert (cwd / project_folder / "notebooks").is_dir()
        assert (cwd / project_folder / "tests").is_dir()
        assert (cwd / project_folder / "src" / f"clustering_{file_name}.py").is_file()
        assert lib_name in get_pip_libraries(cwd / project_folder)

    except Exception as e:
        pytest.fail("Raised exception", e)
    finally:
        teardown()
