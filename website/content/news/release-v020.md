---
title: Release v0.2.0 - Better syntactic parsing and high-quality evaluations
date: "2025-01-15"
---

Hi everyone, I am excited to release the v0.2.0 models for calamanCy.
This has been a long time coming as I've been preparing for this release since the end of 2023.
I am excited to highlight three features for this version:

1. **Improved syntactic parsing from a larger treebank.** Before, we're training our dependency parser and morphological annotation models using a smaller treebank (~150 examples combined). Now, we have access to [UD-NewsCrawl](https://huggingface.co/datasets/UD-Filipino/UD_Tagalog-NewsCrawl), an expert-annotated treebank with 100x more examples! This allows us to train better syntactic parsing models for dependency parsing, POS tagging, and morphological annotation!

2. **New trainable lemmatizer component.** Due to the larger treebank, we now have the means to train a lemmatizer using spaCy's [neural edit-tree lemmatization](https://explosion.ai/blog/edit-tree-lemmatizer) approach.
   This lemmatizer removes the need to handcraft rules and rely solely on statistical methods.
