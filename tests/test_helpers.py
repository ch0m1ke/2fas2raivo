import pytest
from pathlib import Path
import tempfile
from src.helpers import get_2fas_files, get_file_to_process, convert_2fas_to_raivo


@pytest.mark.parametrize(
    ("directory", "expected_result"),
    [
        pytest.param(
            "backups",
            ["backup_unencrypted.2fas", "backup_encrypted.2fas"],
            id="diretory_containing_backups",
        ),
        pytest.param("", [], id="empty_directory"),
    ],
)
def test_get_2fas_files(test_data_directory, directory, expected_result):
    backup_dir = Path.joinpath(test_data_directory, directory)
    twofas_files = [path.name for path in get_2fas_files(backup_dir)]
    assert twofas_files == expected_result


@pytest.mark.parametrize(
    ("directory", "error_type"),
    [
        pytest.param(
            "backups",
            TypeError,
            id="src_dir_is_not_path_object",
        ),
        pytest.param(
            Path("/tmp_dir"),
            ValueError,
            id="src_dir_is_not_valid_directory",
        ),
    ],
)
def test_get_2fas_files_error(directory, error_type):
    with pytest.raises(error_type):
        twofas_files = [path.name for path in get_2fas_files(directory)]


@pytest.mark.parametrize(
    ("files_list", "selection", "expected_result"),
    [
        pytest.param(
            [Path("backup_unencrypted.2fas"), Path("backup_encrypted.2fas")],
            0,
            Path("backup_unencrypted.2fas"),
            id="select_unencrypted_backup",
        ),
        pytest.param(
            [Path("backup_unencrypted.2fas"), Path("backup_encrypted.2fas")],
            1,
            Path("backup_encrypted.2fas"),
            id="select_encrypted_backup",
        ),
    ],
)
def test_get_file_to_process(monkeypatch, files_list, selection, expected_result):
    def mock_selection(prompt):
        return selection

    monkeypatch.setattr("builtins.input", mock_selection)
    result = get_file_to_process(files_list)
    assert result == expected_result


@pytest.mark.parametrize(
    ("files_list", "selection"),
    [pytest.param([], 0, id="select_backup_error")],
)
def test_get_file_to_process_error(monkeypatch, files_list, selection):
    def mock_selection(prompt):
        return selection

    monkeypatch.setattr("builtins.input", mock_selection)
    with pytest.raises(ValueError):
        result = get_file_to_process(files_list)


@pytest.mark.parametrize(
    ("src_file", "dst_file", "password"),
    [
        pytest.param(
            "backup_unencrypted.2fas",
            "raivo_export.zip",
            None,
            id="convert_unencrypted_backup",
        ),
        pytest.param(
            "backup_encrypted.2fas",
            "raivo_export_encrypted.zip",
            "test123",
            id="convert_encrypted_backup",
        ),
    ],
)
def test_convert_2fas_to_raivo(test_data_directory, src_file, dst_file, password):
    src = test_data_directory.joinpath("backups", src_file)
    with tempfile.TemporaryDirectory(dir=test_data_directory) as temp_dir:
        dst = Path(temp_dir).joinpath(dst_file)
        convert_2fas_to_raivo(src, dst, password)
        assert dst.exists(), f"Expected file {dst.name} not found in {temp_dir}"


@pytest.mark.parametrize(
    ("src_file", "dst_file", "password", "exception"),
    [
        pytest.param(
            "backup.2fas",
            "raivo_export.zip",
            None,
            FileNotFoundError,
            id="convert_backup_file_not_found",
        )
    ],
)
def test_convert_2fas_to_raivo_error(
    test_data_directory, src_file, dst_file, password, exception
):
    src = test_data_directory.joinpath("backups", src_file)
    with tempfile.TemporaryDirectory(dir=test_data_directory) as temp_dir:
        with pytest.raises(exception):
            dst = Path(temp_dir).joinpath(dst_file)
            convert_2fas_to_raivo(src, dst, password)
