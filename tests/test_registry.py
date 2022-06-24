import pytest
from .utils import TEST_FOLDER
from gryphon.core.registry import \
    RegistryCollection, GitRegistry, \
    LocalRegistry, TemplateRegistry


TEST_REPO = "https://github.com/vittorfp/template_registry.git"


def test_template_registry_1():
    registry_path = TEST_FOLDER / "data" / "ok_registry"
    registry = TemplateRegistry(templates_root=registry_path)

    metadata = registry.get_templates()
    assert "init" in metadata
    assert "generate" in metadata
    assert "sample_init_" in metadata["init"]
    assert "sample_generate_" in metadata["generate"]


def test_template_registry_2(capfd):
    registry_path = TEST_FOLDER / "data" / "no_metadata_registry"

    TemplateRegistry(templates_root=registry_path)

    captured = capfd.readouterr()
    assert "does not contain a metadata.json file." in captured.out


def test_template_registry_3(capsys, caplog):
    registry_path = TEST_FOLDER / "data" / "wrong_json_registry"

    TemplateRegistry(templates_root=registry_path)

    captured = capsys.readouterr()
    assert "has a malformed json on metadata.json file" in captured.out


def test_template_registry_4():
    registry_path = TEST_FOLDER / "data" / "ok_registry"

    registry = TemplateRegistry(templates_root=registry_path)

    with pytest.raises(NotImplementedError):
        registry.update_registry()


def test_local_registry_1(setup, teardown):
    _ = setup()
    registry_name = "ok_registry"
    data_folder = TEST_FOLDER / "data" / registry_name
    try:
        registry = LocalRegistry(
            templates_root=data_folder,
            registry_name=registry_name,
        )

        metadata = registry.get_templates()
        assert "init" in metadata
        assert "generate" in metadata
        assert "sample_init_local" in metadata["init"]
        assert "sample_generate_local" in metadata["generate"]

    finally:
        teardown()


def test_git_registry_1(setup, teardown):
    cwd = setup()

    registry_name = "ok_registry"
    try:
        registry = GitRegistry(
            registry_url=TEST_REPO,
            registry_folder=cwd,
            registry_name=registry_name
        )
        metadata = registry.get_templates()
        assert "init" in metadata
        assert "generate" in metadata
        assert "basic_analytics_git" in metadata["init"]
        assert "explore_data_basic_git" in metadata["generate"]

        assert "init" in metadata
        assert "generate" in metadata
        assert "basic_analytics_git" in metadata["init"]
        assert "explore_data_basic_git" in metadata["generate"]

        registry = GitRegistry(
            registry_url=TEST_REPO,
            registry_folder=cwd,
            registry_name=registry_name
        )
        metadata = registry.get_templates()
        assert "init" in metadata
        assert "generate" in metadata
        assert "basic_analytics_git" in metadata["init"]

        # TODO: Create sample git repository to make a more reproducible test.
    finally:
        teardown()


def test_registry_collection_1(setup, teardown):
    cwd = setup()
    try:
        configurations = {
            "git_registry": {
                "open-source": TEST_REPO,
                # "ow-private": ""
            },
            "local_registry": {
                "default_registry": TEST_FOLDER / "data" / "ok_registry"
            }
        }
        registry = RegistryCollection.from_config_file(configurations, cwd)

        metadata = registry.get_templates()

        assert "sample_init_local" in metadata['init']

    finally:
        teardown()


def test_registry_collection_2(setup, teardown):
    cwd = setup()
    try:
        configurations = {
            "local_registry": {
                "default_registry": TEST_FOLDER / "data" / "ok_registry",
                "registry_2": TEST_FOLDER / "data" / "ok_registry"
            }
        }

        try:
            RegistryCollection.from_config_file(configurations, cwd)
        except ValueError as e:
            assert "Check your registries to deduplicate" in str(e)
    finally:
        teardown()
