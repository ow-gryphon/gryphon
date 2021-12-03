from os import path
import pytest
from .utils import TEST_FOLDER
from labskit_commands.registry import \
    RegistryCollection, GitRegistry, \
    LocalRegistry, TemplateRegistry


def test_template_registry_1():
    registry_path = path.join(TEST_FOLDER, "data", "ok_registry")
    registry = TemplateRegistry(templates_path=registry_path)

    metadata = registry.get_metadata()
    assert "init" in metadata
    assert "generate" in metadata
    assert "sample_init" in metadata["init"]
    assert "sample_generate" in metadata["generate"]


def test_template_registry_2(capsys):
    registry_path = path.join(TEST_FOLDER, "data", "no_metadata_registry")

    registry = TemplateRegistry(templates_path=registry_path)
    registry.get_metadata()

    captured = capsys.readouterr()
    assert "WARNING" in captured.out
    assert "does not contain a metadata.json file." in captured.out


def test_template_registry_3(capsys):
    registry_path = path.join(TEST_FOLDER, "data", "wrong_json_registry")

    registry = TemplateRegistry(templates_path=registry_path)
    registry.get_metadata()

    captured = capsys.readouterr()
    assert "WARNING" in captured.out
    assert "has a malformed json on metadata.json file" in captured.out


def test_template_registry_4():
    registry_path = path.join(TEST_FOLDER, "data", "ok_registry")

    registry = TemplateRegistry(templates_path=registry_path)

    with pytest.raises(NotImplementedError):
        registry.update_registry()


def test_local_registry_1(setup, teardown):
    cwd = setup()
    registry_name = "ok_registry"
    data_folder = path.join(TEST_FOLDER, "data", registry_name)
    try:
        registry = LocalRegistry(
            registry_origin=data_folder,
            registry_name=registry_name,
            registry_folder=cwd
        )

        metadata = registry.get_metadata()
        assert "init" in metadata
        assert "generate" in metadata
        assert "sample_init" in metadata["init"]
        assert "sample_generate" in metadata["generate"]

        destiny_register = path.join(cwd, registry_name)
        destiny_init = path.join(destiny_register, "init")
        destiny_generate = path.join(destiny_register, "generate")

        assert path.isdir(destiny_register)
        assert path.isdir(destiny_init)
        assert path.isdir(destiny_generate)

        registry.update_registry()

        assert path.isdir(destiny_register)
        assert path.isdir(destiny_init)
        assert path.isdir(destiny_generate)

    finally:
        teardown()


def test_git_registry_1(setup, teardown):
    cwd = setup()

    registry_name = "ok_registry"
    try:
        registry = GitRegistry(
            registry_url="https://github.com/vittorfp/template_registry.git",
            registry_folder=cwd,
            registry_name=registry_name
        )
        metadata = registry.get_metadata()
        assert "init" in metadata
        assert "generate" in metadata
        assert "fancy_git_analytics" in metadata["init"]
        assert "fancy_git_clustering" in metadata["generate"]

        destiny_register = path.join(cwd, registry_name)
        destiny_init = path.join(destiny_register, "init")
        destiny_generate = path.join(destiny_register, "generate")

        assert path.isdir(destiny_register)
        assert path.isdir(destiny_init)
        assert path.isdir(destiny_generate)

        registry.update_registry()
        metadata = registry.get_metadata()

        assert "init" in metadata
        assert "generate" in metadata
        assert "fancy_git_analytics" in metadata["init"]
        assert "fancy_git_clustering" in metadata["generate"]

        assert path.isdir(destiny_register)
        assert path.isdir(destiny_init)
        assert path.isdir(destiny_generate)

        registry = GitRegistry(
            registry_url="https://github.com/vittorfp/template_registry.git",
            registry_folder=cwd,
            registry_name=registry_name
        )
        metadata = registry.get_metadata()
        assert "init" in metadata
        assert "generate" in metadata
        assert "fancy_git_analytics" in metadata["init"]
        assert "fancy_git_clustering" in metadata["generate"]

        # TODO: Create sample git repository to make a more realistic test.
    finally:
        teardown()


def test_registry_collection_1(setup, teardown):
    cwd = setup()
    try:
        configurations = {
            "git_registry": {
                "open-source": "https://github.com/vittorfp/template_registry.git",
                "ow-private": ""
            },
            "local_registry": {
                "default_registry": path.join(TEST_FOLDER, "data", "ok_registry")
            }
        }
        registry = RegistryCollection.from_config_file(configurations, cwd)

        git_registry = path.join(cwd, "open-source")
        local_registry = path.join(cwd, "default_registry")
        git_registry_init = path.join(git_registry, "init")
        git_registry_generate = path.join(git_registry, "generate")
        local_registry_init = path.join(local_registry, "init")
        local_registry_generate = path.join(local_registry, "generate")

        assert path.isdir(git_registry)
        assert path.isdir(local_registry)
        assert path.isdir(git_registry_init)
        assert path.isdir(git_registry_generate)
        assert path.isdir(local_registry_init)
        assert path.isdir(local_registry_generate)

        metadata = registry.get_metadata()

        assert "fancy_git_analytics" in metadata['init']
        assert "sample_init" in metadata['init']

    finally:
        teardown()


def test_registry_collection_2(setup, teardown):
    cwd = setup()
    try:
        configurations = {
            "local_registry": {
                "default_registry": path.join(TEST_FOLDER, "data", "ok_registry"),
                "registry_2": path.join(TEST_FOLDER, "data", "ok_registry")
            }
        }
        with pytest.raises(ValueError):
            RegistryCollection.from_config_file(configurations, cwd)

    finally:
        teardown()
