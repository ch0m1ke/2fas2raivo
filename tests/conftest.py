import pytest
from pathlib import Path


@pytest.fixture
def test_data_directory():
    cwd = Path.cwd()
    test_data_dir = Path.joinpath(cwd, "tests", "test_data")
    return test_data_dir
