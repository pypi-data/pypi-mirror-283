import pytest
import pandas as pd
import tempfile
import shutil
from pathlib import Path

import pardos

@pytest.fixture(scope="module")
def sample_data():
    with tempfile.TemporaryDirectory() as tmpdir:
        base_dir = Path(tmpdir)
        paths = [
            base_dir / "file1.txt",
            base_dir / "file2.txt",
            base_dir / "dir1",
        ]
        for path in paths:
            if str(path).endswith(".txt"):
                path.touch()
            else:
                path.mkdir()
        yield base_dir, paths

        # Clean up
        for path in paths:
            if path.is_file():
                path.unlink()
            elif path.is_dir():
                shutil.rmtree(path)

@pytest.fixture
def sample_series(sample_data):
    _, paths = sample_data
    return pd.Series(paths)

def test_unix_accessor_initialization(sample_series):
    assert hasattr(sample_series, 'unix'), "Series should have 'unix' accessor"

def test_rm(sample_data, sample_series):
    base_dir, _ = sample_data
    sample_series.unix.rm()
    assert not any(path.exists() for path in sample_series)

    # Recreate files for other tests
    for path in sample_series:
        if str(path).endswith(".txt"):
            path.touch()
        else:
            path.mkdir()

def test_cp(sample_data, sample_series):
    base_dir, _ = sample_data
    with tempfile.TemporaryDirectory() as dest:
        result = sample_series.unix.cp(dest).tolist()
        assert all(Path(dest) / path.name in result for path in sample_series)
        assert all(path.exists() for path in result)

def test_mv(sample_data, sample_series):
    base_dir, _ = sample_data
    with tempfile.TemporaryDirectory() as dest:
        result = sample_series.unix.mv(dest).tolist()
        assert all(Path(dest) / path.name in result for path in sample_series)
        assert all(path.exists() for path in result)
        assert not any(path.exists() for path in sample_series)

    # Recreate files for other tests
    for path in sample_series:
        if str(path).endswith(".txt"):
            path.touch()
        else:
            path.mkdir()

def test_ln(sample_data, sample_series):
    base_dir, _ = sample_data
    with tempfile.TemporaryDirectory() as dest:
        result = sample_series.unix.ln(dest).tolist()
        assert all(Path(dest) / path.name in result for path in sample_series)
        assert all(path.is_symlink() for path in result)

# Add more tests as needed
