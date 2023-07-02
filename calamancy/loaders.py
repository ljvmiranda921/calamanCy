"""Functionality for downloading calamanCy models"""

import subprocess
import sys
from typing import Dict, List

import spacy
from spacy.util import get_installed_models
from wasabi import msg


def _get_models_url() -> Dict[str, str]:
    """Get a mapping of each calamanCy pipeline (versioned) and their download links

    This will be actively maintained to ensure that the latest versions are
    tracked and the download functions below work as expected.
    """
    return {
        "tl_calamancy_md-0.1.0": "https://huggingface.co/ljvmiranda921/tl_calamancy_md/resolve/55ef01a244f3ca77676de6ba5a2beea0ba3e0021/tl_calamancy_md-any-py3-none-any.whl",
        "tl_calamancy_lg-0.1.0": "https://huggingface.co/ljvmiranda921/tl_calamancy_lg/resolve/55ef01a244f3ca77676de6ba5a2beea0ba3e0021/tl_calamancy_lg-any-py3-none-any.whl",
        "tl_calamancy_trf-0.1.0": "https://huggingface.co/ljvmiranda921/tl_calamancy_trf/resolve/55ef01a244f3ca77676de6ba5a2beea0ba3e0021/tl_calamancy_trf-any-py3-none-any.whl",
    }


def _get_name(model: str) -> str:
    return model.split("-")[0]


def _get_version(model: str) -> str:
    return model.split("-")[-1]


def get_latest_version(model: str) -> str:
    """Return the latest version of a calamanCy model.

    model (str): string indicating the model.
    RETURNS (str): latest version of the model.
    """
    models_url = _get_models_url()
    compat = [model_name for model_name in models_url if model_name.startswith(model)]
    versions = sorted(
        [_get_version(model) for model in compat],
        key=lambda s: [int(u) for u in s.split(".")],
        reverse=True,
    )
    return versions[0]


def models() -> List[str]:
    """Get a list of valid calamanCy models.

    RETURNS (List[str]): list of valid calamanCy models.
    """
    models_url = _get_models_url()
    return list(models_url.keys())


def load(model: str, force: bool = False, **kwargs) -> "spacy.language.Language":
    """Load a calamanCy model as a spaCy language pipeline.

    If the model is not downloaded, it will also download and install it.
    You can use the 'force' keyword argument to force downloading an existing model.

    model (str): the model to download. See the available models at calamancy.models().
    force (bool): force download the model. Defaults to False.
    kwargs: additional arguments to spacy.load().
    RETURNS (Language): a spaCy language pipeline.
    """
    model_name = download_model(model, force=force)
    return spacy.load(model_name, **kwargs)


def install(package: str):
    """Install a calamanCy package."""
    subprocess.run(
        [sys.executable, "-m", "pip", "install", package, "--no-deps"],
        check=True,
    )


def download_model(model: str, force: bool = False, verbose: bool = False) -> str:
    """Download and install a specified calamanCy pipeline.

    model (str): string indicating calamanCy model. Use calamancy.models() to
        get a list of valid models.
    force (bool): force download the model. Defaults to False.
    verbose (bool): set the verbosity of this command. Defaults to False.
    RETURNS (str): path to the model location.
    """
    models_url = _get_models_url()
    if model not in models_url:
        raise ValueError(
            f"The model '{model}' is not available in calamanCy. "
            f"Available models are: {','.join(m for m in models())}"
        )

    # Check if model has already been installed and other flags
    model_is_installed = _get_name(model) in get_installed_models()
    if model_is_installed and not force:
        msg.text(f"Model '{model}' is already installed.", show=verbose)
        return _get_name(model)

    msg.info(f"Installing '{model}' from {models_url[model]}...")
    install(models_url[model])
    return _get_name(model)
