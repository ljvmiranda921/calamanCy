import pytest

from calamancy import loaders


@pytest.fixture
def mock_models_url(monkeypatch):
    """loaders._get_models_url mocked to return constant, unchanging, values."""
    test_models_url = {
        "test_model_md-0.1.0": "example.com",
        "test_model_md-0.2.0": "example.com",
        "test_model_lg-0.1.0": "example.com",
    }
    monkeypatch.setattr(loaders, "_get_models_url", lambda: test_models_url)


@pytest.fixture
def mock_install(monkeypatch):
    """loaders.install mocked to just return true, no installation happens."""
    monkeypatch.setattr(loaders, "install", lambda x: True)


@pytest.mark.parametrize(
    "query,expected",
    [("test_model_lg", "0.1.0"), ("test_model_md", "0.2.0")],
)
def test_latest_version_returns_expected(mock_models_url, query, expected):
    result = loaders.get_latest_version(model=query)
    assert result == expected


@pytest.mark.parametrize("force", [True, False])
def test_download_model_returns_name(mock_install, mock_models_url, force):
    model_name = loaders.download_model("test_model_md-0.1.0", force=force)
    assert model_name == "test_model_md"


def test_download_model_errors_when_invalid():
    with pytest.raises(ValueError):
        loaders.download_model(model="invalid_model")
