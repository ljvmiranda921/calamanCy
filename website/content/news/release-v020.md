---
title: Release v0.2.0 - Better syntactic parsing and high-quality evaluations
date: "2025-01-15"
---

Hi everyone, I am excited to release the v0.2.0 models for calamanCy.
This has been a long time coming as I've been preparing for this release since the end of 2023.
I am excited to highlight three features for this version:

1. **Improved syntactic parsing from a larger treebank.** Before, we're training our dependency parser and morphological annotation models using a smaller treebank (~150 examples combined). Now, we have access to [UD-NewsCrawl](https://huggingface.co/datasets/UD-Filipino/UD_Tagalog-NewsCrawl), an expert-annotated treebank with 100x more examples! This allows us to train better syntactic parsing models for dependency parsing, POS tagging, and morphological annotation!

2. **Updated spaCy components.** Due to the larger treebank, we now have the means to train a lemmatizer using spaCy's [neural edit-tree lemmatization](https://explosion.ai/blog/edit-tree-lemmatizer) approach.
   This lemmatizer removes the need to handcraft rules and rely solely on statistical methods.
   In addition, the [`tl_calamancy_trf`](https://huggingface.co/ljvmiranda921/tl_calamancy_trf) pipeline now uses the modern [mDeBERTa-v3](https://huggingface.co/microsoft/mdeberta-v3-base) pretrained model as its base.

3. **New NER evaluations.** New datasets have been built since the [last release of calamanCy](/calamanCy/news/release-v010/) and I've incorporated them here. This includes [Universal NER](https://www.universalner.org/) (Mayhew et al., 2024) and [TF-NERD](https://dl.acm.org/doi/abs/10.1145/3639233.3639341) (Ramos et al., 2024). I've also removed the TRG and Ugnayan treebanks from the training set and treated them as test sets (as they should be).

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

#### UD-NewsCrawl (test split) results

This treebank consists of annotated text extracted from the Leipzig Tagalog Corpus. 
Data included in the Leipzig Tagalog Corpus were crawled from Tagalog-language online news sites by the Leipzig University Institute for Computer Science.

| Model            |   Token Acc. |   Lemma Acc. |   Tag Acc. |   POS  |   Morph Acc. |   Dep UAS |   Dep LAS |
|:-----------------|------------:|------------:|----------:|----------:|------------:|----------:|----------:|
| [tl_calamancy_md](https://huggingface.co/ljvmiranda921/tl_calamancy_md)  |       95.01 |       90.09 |     90.85 |     95    |       95.34 |     83.45 |     77.13 |
| [tl_calamancy_lg](https://huggingface.co/ljvmiranda921/tl_calamancy_lg)  |       95.01 |       89.79 |     90.62 |     94.99 |       95.04 |     82.9  |     76.5  |
| [tl_calamancy_trf](https://huggingface.co/ljvmiranda921/tl_calamancy_trf) |       95.01 |       90.46 |     91.34 |     95.43 |       95.32 |     85.09 |     78.83 |



#### UD-TRG results

This treebank was manually annotated using sentences from a grammar book.
The Tagalog treebank, so far, consists of 55 sentences with sources from the grammar books Tagalog Reference Grammar (Schachter and Otanes 1972) and Essential Tagalog Grammar: A Reference for Learners of Tagalog (De Vos 2010). The annotations are done manually.

| Model            |   Token Acc. |   Lemma Acc. |   Tag Acc. |   POS  |   Morph Acc. |   Dep UAS |   Dep LAS |
|:-----------------|------------:|------------:|----------:|----------:|------------:|----------:|----------:|
| [tl_calamancy_md](https://huggingface.co/ljvmiranda921/tl_calamancy_md)  |      100    |       79.84 |     58.17 |     78.2  |       73.16 |     93.29 |     66.94 |
| [tl_calamancy_lg](https://huggingface.co/ljvmiranda921/tl_calamancy_lg) |      100    |       78.88 |     56.68 |     77.93 |       71.53 |     94.28 |     67.61 |
| [tl_calamancy_trf](https://huggingface.co/ljvmiranda921/tl_calamancy_trf) |      100    |       80.79 |     58.31 |     78.47 |       72.89 |     94.95 |     67.77 |

#### UD-Ugnayan results

Ugnayan is a manually annotated Tagalog treebank currently composed of educational fiction and nonfiction text. 
The treebank is under development at the University of the Philippines.

| Model            |   Token Acc. |   Lemma Acc. |   Tag Acc. |   POS  |   Morph Acc. |   Dep UAS |   Dep LAS |
|:-----------------|------------:|------------:|----------:|----------:|------------:|----------:|----------:|
| [tl_calamancy_md](https://huggingface.co/ljvmiranda921/tl_calamancy_md)  |       98.08 |       82.29 |     49.16 |     82.82 |       59.41 |     79.7  |     57.32 |
| [tl_calamancy_lg](https://huggingface.co/ljvmiranda921/tl_calamancy_lg)  |       98.08 |       82.29 |     48.58 |     81.67 |       58.95 |     80.92 |     58.47 |
| [tl_calamancy_trf](https://huggingface.co/ljvmiranda921/tl_calamancy_trf) |       98.08 |       82.55 |     48.48 |     82.21 |       58.75 |     80.78 |     58.61 |


## Updated spaCy components

This release also updates the [spaCy components](https://spacy.io/usage/processing-pipelines) included in the pipelines.
Think of a component as a specific step of a pipeline that performs a particular task, such as [POS tagging](https://spacy.io/api/tagger) or [named-entity recognition](https://spacy.io/api/entityrecognizer).
For v0.2.0, we added a new [trainable lemmatizer](https://spacy.io/api/edittreelemmatizer) to take advantage of the treebank we acquired.

In addition, we also updated the transformer model and moved on from RoBERTa Tagalog (which served us quite well in the first release) to mDeBERTa.
From internal experiments, we saw that the updated multilingual transformer served as a more performance base model than a Tagalog-focused one.

You can definitely see performance improvemnts across our previous benchmarks when comparing the previous versions of the transformer-based pipeline on TLUnifed-NER (NER), Hatespeech (binary text categorization) and Dengue (mutilabel text categorization) datasets:

| Model            |   NER (TLUnified-NER) | Binary textcat (Hatespeech) | Multilabel textcat (Dengue)
|:-----------------|---------:|-----:| ----|
| tl_calamancy_trf v0.1.0  |    90.34 | 78.25 | 72.45 |
| tl_calamancy_trf v0.2.0  |    **93.31** | **84.54** | **79.00** |

## New NER evaluations

Finally, I also added new NER evaluations based on new datasets published within the past year.
One of which, [Universal NER](https://arxiv.org/abs/2311.09122), is a project I contributed to.
It is a fun project&mdash; the goal is to follow the footsteps of Universal Dependencies and create a single annotation schema for NER.

For Tagalog, we took the existing treebanks back then (TRG and Ugnayan) and annotated them in a [common annotation guideline](https://www.universalner.org/guidelines/).
Since UD-NewsCrawl is a new treebank, there are still no NER annotations for it yet.
If you're interested to help out and annotate NewsCrawl for NER, then [let us know](https://www.universalner.org/)! 

| Model            |  P (TRG) | R (TRG) |F (TRG) | P (Ugnayan) | R (Ugnayan) | F (Ugnayan)
|:-----------------|---------:|---------:|---------:| ---:| -----:| ----:|
| [tl_calamancy_md](https://huggingface.co/ljvmiranda921/tl_calamancy_md) |    57.5  |   100    |    73.02 | 58.97 | 69.70 | 63.89 |
| [tl_calamancy_lg](https://huggingface.co/ljvmiranda921/tl_calamancy_lg)  |   100    |    95.65 |    97.78 | 60.47 | 78.79 | 68.42 |
| [tl_calamancy_trf](https://huggingface.co/ljvmiranda921/tl_calamancy_trf)|   100    |    95.65 |    97.78 | 63.64 | 84.84 | 72.73 |

I also find this very interesting NER dataset called TF-NERD, which includes more named entity labels than PER (person), ORG (organization), and LOC (location).
For the evals below, I only evaluation on the three labels I had and converted all GPE (geopolitical entities) into LOC for fairness.

| model            |  P (TF-NERD) | R (TF-NERD) |  F (TF-NERD) |
|:-----------------|---------:|---------:|---------:|
| [tl_calamancy_md](https://huggingface.co/ljvmiranda921/tl_calamancy_md)  |    68.36 |    70.78 |    69.55 |
| [tl_calamancy_lg](https://huggingface.co/ljvmiranda921/tl_calamancy_lg) |    67.26 |    70.58 |    68.88 |
| [tl_calamancy_trf](https://huggingface.co/ljvmiranda921/tl_calamancy_trf) |    72.28 |    80.54 |    76.18 |


## Final thoughts

And that's it! 
