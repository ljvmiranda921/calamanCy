"""
This module provides lightweight utility classes for users who are not familiar
with the spaCy primitives. For training, we recommend following the typical
procedure as outlined in the spaCy docs: https://spacy.io/usage/training
"""

from typing import Iterable, Tuple

from .loaders import load


class EntityRecognizer:
    def __init__(self, model: str):
        """Initialize the named entity recognizer

        model (str): the model name.
        """
        self.nlp = load(model)

    def __call__(self, text: str) -> Iterable[Tuple[str, str]]:
        """Return the predicted entities in IOB format for a single text.

        texts (str): the text to get the entities from.
        YIELDS (Iterable[Tuple[str, str]]): the token and its entity (IOB format).
        """
        doc = self.nlp(text)
        for token in doc:
            label = (
                f"{token.ent_iob_}-{token.ent_type_}" if token.ent_iob_ != "O" else "O"
            )
            yield (token.text, label)


class Tagger:
    def __init__(self, model: str):
        """Initialize the parts-of-speech tagger

        model (str): the model name.
        """
        self.nlp = load(model)

    def __call__(self, text: str) -> Iterable[Tuple[str, Tuple[str, str]]]:
        """Return the coarse-grained and fine-grained parts-of-speech (POS) tag.

        texts (str): the text to get the POS tags from.
        YIELDS (Iterable[Tuple[str, str, str]]): the token and its coarse-grained and fine-grained POS tag.
        """
        doc = self.nlp(text)
        for token in doc:
            yield (token.text, (token.pos_, token.tag_))


class Parser:
    def __init__(self, model: str):
        """Initialize the dependency parser

        model (str): the model name.
        """
        self.nlp = load(model)

    def __call__(self, text: str) -> Iterable[Tuple[str, str]]:
        """Return the syntactic dependency relation for a given token.

        text (str): the text to get the dependency relations from.
        YIELDS (Iterable[Tuple[str, str]]): the token and its dependency relation.
        """
        doc = self.nlp(text)
        for token in doc:
            yield (token.text, token.dep_)
