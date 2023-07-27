import pytest

from calamancy import EntityRecognizer, Parser, Tagger

tasks = [EntityRecognizer, Tagger, Parser]


@pytest.fixture
def text():
    return "Ako si Juan de la Cruz"


@pytest.fixture
def calamancy_md():
    return "tl_calamancy_md-0.1.0"


@pytest.mark.parametrize("task", [EntityRecognizer, Tagger, Parser])
def test_api_is_working(task, text, calamancy_md):
    """Functional test to check if API contract is followed"""
    fn = task(model=calamancy_md)
    preds = list(fn.predict(text))
    assert len(preds) == len(text.split(" "))
