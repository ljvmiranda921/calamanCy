---
title: Release v0.2.0 - Better syntactic parsing and high-quality evaluations
date: "2025-01-15"
---

Hi everyone, I am excited to release the v0.2.0 models for calamanCy.
This has been a long time coming as I've been preparing for this release since the end of 2023.
I am excited to highlight three features for this version:

1. **Improved syntactic parsing from a larger treebank.** Before, we're training our dependency parser and morphological annotation models using a smaller treebank (~150 examples combined). Now, we have access to [UD-NewsCrawl](https://huggingface.co/datasets/UD-Filipino/UD_Tagalog-NewsCrawl), an expert-annotated treebank with 100x more examples! This allows us to train better syntactic parsing models for dependency parsing, POS tagging, and morphological annotation!

2. **Modern spaCy components.** Due to the larger treebank, we now have the means to train a lemmatizer using spaCy's [neural edit-tree lemmatization](https://explosion.ai/blog/edit-tree-lemmatizer) approach.
   This lemmatizer removes the need to handcraft rules and rely solely on statistical methods.
   In addition, the [`tl_calamancy_trf`](https://huggingface.co/ljvmiranda921/tl_calamancy_trf) pipeline now uses the modern [mDeBERTa-v3](https://huggingface.co/microsoft/mdeberta-v3-base) pretrained model as its base.

3. **More evaluations.** New datasets have been built since the [last release of calamanCy](/calamanCy/news/release-v010/) and I've incorporated them here. This includes [Universal NER](https://www.universalner.org/) (Mayhew et al., 2024) and [TF-NERD](https://dl.acm.org/doi/abs/10.1145/3639233.3639341) (Ramos et al., 2024). I've also removed the TRG and Ugnayan treebanks from the training set and treated them as test sets (as they should be).

You can find all the models in this [HuggingFace collection](https://huggingface.co/collections/ljvmiranda921/calamancy-models-for-tagalog-nlp-65629cc46ef2a1d0f9605c87):

| Model                                                                              | Pipelines                                                             | Description                                                                            |
| ---------------------------------------------------------------------------------- | --------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| [tl_calamancy_md](https://huggingface.co/ljvmiranda921/tl_calamancy_md) (214 MB)   | tok2vec, tagger, trainable_lemmatizer, morphologizer, parser, ner     | CPU-optimized Tagalog NLP model. Using floret vectors (50k keys)                       |
| [tl_calamancy_lg](https://huggingface.co/ljvmiranda921/tl_calamancy_lg) (482 MB)   | tok2vec, tagger, trainable_lemmatizer, morphologizer, parser, ner     | CPU-optimized large Tagalog NLP model. Using fastText vectors (714k)                   |
| [tl_calamancy_trf](https://huggingface.co/ljvmiranda921/tl_calamancy_trf) (1.7 GB) | transformer, tagger, trainable_lemmatizer, morphologizer, parser, ner | GPU-optimized transformer Tagalog NLP model. Uses mdeberta-v3-base as context vectors. |

## Improved syntactic parsing from a larger treebank

One of the biggest updates in v0.2.0 is that we're now using the [UD-NewsCrawl treebank](https://huggingface.co/datasets/UD-Filipino/UD_Tagalog-NewsCrawl) for our syntactic parsing models.
This treebank contains 15,000 sentences with expert annotations on dependency relations, morphology, and tokenization&mdash; a huge jump from the ~150 examples we had before.

<iframe
  src="https://huggingface.co/datasets/UD-Filipino/UD_Tagalog-NewsCrawl/embed/viewer"
  frameborder="0"
  width="100%"
  height="560px"
></iframe>

This is all thanks to the annotation efforts made by [Elsie Or](https://linguistics.upd.edu.ph/building-a-tagalog-universal-dependencies-treebank/), [Angelina Aquino](https://angelaquino.github.io/), and their [team](https://linguistics.upd.edu.ph/building-a-tagalog-universal-dependencies-treebank/) from the University of the Philippines!
I was also partly involved in the project, focusing on post-processing and on training the baseline dependency parsers, so expect a paper from us soon!

All the v0.2.0 models now use the UD-NewsCrawl treebank as their training set. I've also retired the TRG and Ugnayan treebanks and designated them as test sets for evaluation. Below, you'll find the syntactic parsing results for (1) the test split of UD-NewsCrawl and (2) the full datasets of TRG and Ugnayan.

## Modern spaCy components

## More evaluations

## What's next?
