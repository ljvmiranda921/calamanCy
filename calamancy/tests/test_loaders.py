import pytest

from calamancy import loaders


@pytest.fixture
def mock_models(monkeypatch):
    """loaders._get_models mocked to return constant, unchanging, values."""
    test_models = {
        "test_model_md-0.1.0": ("user/test_model_md-0.1.0", "main"),
        "test_model_md-0.2.0": ("user/test_model_md", "0.2.0"),
        "test_model_lg-0.1.0": ("user/test_model_lg-0.1.0", "main"),
    }
    monkeypatch.setattr(loaders, "_get_models", lambda: test_models)


@pytest.fixture
def mock_snapshot_download(monkeypatch):
    """loaders.snapshot_download mocked to return a fake path, no download happens."""
    calls = []

    def _snapshot_download(**kwargs):
        calls.append(kwargs)
        return f"/fake/cache/{kwargs['repo_id']}"

    monkeypatch.setattr(loaders, "snapshot_download", _snapshot_download)
    return calls


@pytest.mark.parametrize(
    "query,expected",
    [("test_model_lg", "0.1.0"), ("test_model_md", "0.2.0")],
)
def test_latest_version_returns_expected(mock_models, query, expected):
    result = loaders.get_latest_version(model=query)
    assert result == expected


@pytest.mark.parametrize("force", [True, False])
def test_download_model_returns_path(mock_snapshot_download, mock_models, force):
    model_path = loaders.download_model("test_model_md-0.1.0", force=force)
    assert model_path == "/fake/cache/user/test_model_md-0.1.0"
    assert mock_snapshot_download[-1]["force_download"] == force


def test_download_model_resolves_unversioned_to_latest(
    mock_snapshot_download, mock_models
):
    loaders.download_model("test_model_md")
    assert mock_snapshot_download[-1]["repo_id"] == "user/test_model_md"
    assert mock_snapshot_download[-1]["revision"] == "0.2.0"


def test_download_model_errors_when_invalid():
    with pytest.raises(ValueError):
        loaders.download_model(model="invalid_model")
