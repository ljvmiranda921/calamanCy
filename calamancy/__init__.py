__version__ = "0.2.2"

from .inference import EntityRecognizer, Parser, Tagger
from .loaders import get_latest_version, load, models

__all__ = [
    "__version__",
    "get_latest_version",
    "models",
    "load",
    # Inference
    "EntityRecognizer",
    "Tagger",
    "Parser",
]
