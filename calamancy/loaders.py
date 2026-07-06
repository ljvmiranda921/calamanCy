"""Functionality for downloading calamanCy models"""

from typing import Dict, List, Tuple

import spacy
from huggingface_hub import snapshot_download
from wasabi import msg


def _get_models() -> Dict[str, Tuple[str, str]]:
    """Get a mapping of each calamanCy pipeline (versioned) to its Hugging Face
    repository and git revision.

    Starting v0.2.0, all versions of a pipeline live in a single repository
    (e.g., ljvmiranda921/tl_calamancy_md) where each release is a git tag and
    'main' points to the latest version. Older versions live in their original
    repositories.
    """
    return {
        "tl_calamancy_md-0.2.0": ("ljvmiranda921/tl_calamancy_md", "0.2.0"),
        "tl_calamancy_lg-0.2.0": ("ljvmiranda921/tl_calamancy_lg", "0.2.0"),
        "tl_calamancy_trf-0.2.0": ("ljvmiranda921/tl_calamancy_trf", "0.2.0"),
        "tl_calamancy_md-0.1.0": ("ljvmiranda921/tl_calamancy_md-0.1.0", "main"),
        "tl_calamancy_lg-0.1.0": ("ljvmiranda921/tl_calamancy_lg-0.1.0", "main"),
        "tl_calamancy_trf-0.1.0": ("ljvmiranda921/tl_calamancy_trf-0.1.0", "main"),
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
    compat = [model_name for model_name in _get_models() if model_name.startswith(model)]
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
    return list(_get_models().keys())


def load(model: str, force: bool = False, **kwargs) -> "spacy.language.Language":
    """Load a calamanCy model as a spaCy language pipeline.

    If the model is not yet in the local Hugging Face cache, it will be
    downloaded first. You can use the 'force' keyword argument to force
    re-downloading a cached model.

    model (str): the model to load. See the available models at
        calamancy.models(). You can also pass an unversioned name
        (e.g., 'tl_calamancy_md') to get its latest version.
    force (bool): force download the model. Defaults to False.
    kwargs: additional arguments to spacy.load().
    RETURNS (Language): a spaCy language pipeline.
    """
    model_path = download_model(model, force=force)
    return spacy.load(model_path, **kwargs)


def download_model(model: str, force: bool = False, verbose: bool = False) -> str:
    """Download a calamanCy pipeline into the local Hugging Face cache.

    Unlike calamanCy < 0.3.0, this no longer installs the model as a Python
    package via pip. Models are fetched with huggingface_hub instead, which
    works in any environment (pip, uv, poetry, conda) and caches downloads
    under the Hugging Face cache directory.

    model (str): string indicating calamanCy model. Use calamancy.models() to
        get a list of valid models. You can also pass an unversioned name
        (e.g., 'tl_calamancy_md') to get its latest version.
    force (bool): force download the model. Defaults to False.
    verbose (bool): set the verbosity of this command. Defaults to False.
    RETURNS (str): path to the model location.
    """
    models_to_repo = _get_models()
    names = {_get_name(m) for m in models_to_repo}
    if model in names:
        model = f"{model}-{get_latest_version(model)}"
    if model not in models_to_repo:
        raise ValueError(
            f"The model '{model}' is not available in calamanCy. "
            f"Available models are: {','.join(m for m in models())}"
        )

    name, version = _get_name(model), _get_version(model)
    latest_version = get_latest_version(name)
    if version != latest_version:
        msg.warn(
            f"You are loading '{model}', but a newer version is available. "
            f"Please upgrade to '{name}-{latest_version}' by passing it to "
            "calamancy.load()."
        )

    repo_id, revision = models_to_repo[model]
    msg.info(
        f"Fetching '{model}' from https://huggingface.co/{repo_id} (revision: {revision})...",
        show=verbose,
    )
    return snapshot_download(
        repo_id=repo_id,
        revision=revision,
        force_download=force,
        # The repositories also host the pipeline as a wheel; skip it because
        # we load directly from the extracted files.
        ignore_patterns=["*.whl"],
    )
