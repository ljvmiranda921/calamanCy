---
title: Release v0.1.0 - Initial Release
date: "2023-08-01"
---

Hi everyone, I'm happy to share the first minor release of calamanCy!

This release adds our first `tl_calamancy` models with varying sizes to suit any performance or accuracy requirements. The table below shows more information about these pipelines.

## Motivation: Tagalog NLP resources are disjointed

Despite Tagalog being a widely-spoken language here in the Philippines, model and data resources are still scarce.
For example, our Universal Dependencies (UD) treebanks are tiny (less than 20k words)
and domain-specific corpora are few and far between.

In addition, we only have limited choices when it comes to Tagalog language models (LMs).
For monolingual LMs, the state-of-the-art is RoBERTa-Tagalog.
For multilingual LMs, we have the usual XLM-RoBERTa and multilingual BERT.
Tagalog is included in their training pool, but these models are still prone to the curse of multilinguality.

Therefore, consolidating these resources and providing more options to build Tagalog NLP pipelines is still an open problem.
This is what I hope and endeavor to solve, as a Filipino and an NLP researcher!

## Presenting the first calamanCy models

The models are also [hosted on Huggingface](https://huggingface.co/ljvmiranda921), but you can also use the `calamancy` library to download and access.

| Model                                                                                | Pipelines                                   | Description                                                                                                       |
| ------------------------------------------------------------------------------------ | ------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| [tl_calamancy_md](https://huggingface.co/ljvmiranda921/tl_calamancy_md-0.1.0) (73.7 MB)    | tok2vec, tagger, morphologizer, parser, ner | CPU-optimized Tagalog NLP model. Pretrained using the TLUnified dataset. Using floret vectors (50k keys)          |
| [tl_calamancy_lg](https://huggingface.co/ljvmiranda921/tl_calamancy_lg-0.1.0) (431.9 MB)   | tok2vec, tagger, morphologizer, parser, ner | CPU-optimized large Tagalog NLP model. Pretrained using the TLUnified dataset. Using fastText vectors (714k keys) |
| [tl_calamancy_trf](https://huggingface.co/ljvmiranda921/tl_calamancy_trf-0.1.0) (775.6 MB) | transformer, tagger, parser, ner            | GPU-optimized transformer Tagalog NLP model. Uses roberta-tagalog-base as context vectors.                        |

## Performance and baselines

Before calamanCy, you usually have two options if you want to build a pipeline for Tagalog: (1) piggyback on a model trained from a linguistically-similar language (**cross-lingual transfer**) or (2) finetune a multilingual LM like XLM-R or multilingual BERT on your data (**multilingual finetuning**). Here, I want to check if calamanCy is competitive enough against these alternatives. I tested on the following tasks and datasets:

| Dataset                                                                                    | Task / Labels                                                             | Description                                                                                                                    |
| ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| Hatespeech ([Cabasag et al., 2019](#cabasag2019hatespeech))                                | Binary text classification (_hate speech, not hate speech_)               | Contains 10k tweets collected during the 2016 Philippine Presidential Elections labeled as hatespeech or non-hate speech.      |
| Dengue ([Livelo and Cheng, 2018](#livelo2018dengue))                                       | Multilabel text classification (_absent, dengue, health, sick, mosquito_) | Contains 4k dengue-related tweets collected for a health infoveillance application that classifies text into dengue subtopics. |
| TLUnified-NER ([Cruz and Cheng, 2021](#cruz2021tlunified))                                 | NER (_Person, Organization, Location_)                                    | A held-out test split from the annotated TLUnified corpora containing news reports.                                            |
| Merged UD ([Aquino and de Leon, 2020](#aquino2020ugnayan); [Samson, 2018](#samson2018trg)) | Dependency parsing and POS tagging                                        | Merged version of the Ugnayan and TRG treebanks from the Universal Dependencies framework.                                     |

For text categorization and NER, I ran the experiments for five trials and reported their average and standard deviation.
For dependency parsing and POS tagging, I used 10-fold cross-validation because the combined UD treebank is still too small.

The results show that our calamanCy pipelines are competitive (you can reproduce the results by following this [spaCy project](https://github.com/ljvmiranda921/calamanCy/tree/master/paper/benchmark)):

<!-- insert results here -->

| Language Pipeline                                                         | Binary textcat (Hatespeech) | Multilabel textcat (Dengue) | NER (TLUnified-NER) | Dependency parsing, UAS (Merged UD) | Dependency parsing, LAS (Merged UD) |
| ------------------------------------------------------------------------- | --------------------------- | --------------------------- | ------------------- | ----------------------------------- | ----------------------------------- |
| [tl_calamancy_md](https://huggingface.co/ljvmiranda921/tl_calamancy_md-0.1.0)   | 74.40 (0.05)                | 65.32 (0.04)                | 87.67 (0.03)        | 76.47                               | 54.40                               |
| [tl_calamancy_lg](https://huggingface.co/ljvmiranda921/tl_calamancy_lg-0.1.0)   | 75.62 (0.02)                | 68.42 (0.01)                | 88.90 (0.01)        | 82.13                               | 70.32                               |
| [tl_calamancy_trf](https://huggingface.co/ljvmiranda921/tl_calamancy_trf-0.1.0) | 78.25 (0.06)                | 72.45 (0.02)                | 90.34 (0.02)        | 92.48                               | 80.90                               |

We also evaluated cross-lingual and multilingual approaches in our benchmarks:

- **Cross-lingual**: we chose the source languages using a WALS-reliant metric (Agic, 2017) to choose the linguistically-closest languages to Tagalog and looked for their corresponding spaCy pipelines.
  We came up with Indonesian (id), Vietnamese (vi), Ukranian (uk), Romanian (ro), and Catalan (ca). However, only uk, ca, ro have spaCy pipelines. We finetuned each dataset for each task and evaluated them similarly to our Tagalog monolingual models.

| Language Pipeline | Binary textcat (Hatespeech) | Multilabel textcat (Dengue) | NER (TLUnified-NER) | Dependency parsing, UAS (Merged UD) | Dependency parsing, LAS (Merged UD) |
| ----------------- | --------------------------- | --------------------------- | ------------------- | ----------------------------------- | ----------------------------------- |
| uk_core_news_trf  | 75.24 (0.05)                | 65.57 (0.01)                | 51.11 (0.02)        | 54.77                               | 37.68                               |
| ro_core_news_lg   | 69.01 (0.01)                | 59.10 (0.01)                | 02.01 (0.00)        | 84.65                               | 65.30                               |
| ca_core_news_trf  | 70.01 (0.02)                | 59.42 (0.03)                | 14.58 (0.02)        | 91.17                               | 79.30                               |

- **Multilingual**: we used XLM RoBERTa and an uncased version of mBERT as our base transformer models. We also finetuned each model for each task and did similar evaluations.
  Note that finetuning on XLM RoBERTa (both base and large versions) may require at least a V100 GPU. I've seen more consistent and stable training with an A100 GPU. Same can be said for mBERT.

| Language Pipeline      | Binary textcat (Hatespeech) | Multilabel textcat (Dengue) | NER (TLUnified-NER) | Dependency parsing, UAS (Merged UD) | Dependency parsing, LAS (Merged UD) |
| ---------------------- | --------------------------- | --------------------------- | ------------------- | ----------------------------------- | ----------------------------------- |
| xlm-roberta-base       | 77.57 (0.01)                | 67.20 (0.01)                | 88.03 (0.03)        | 88.34                               | 76.07                               |
| bert-base-multilingual | 76.40 (0.02)                | 71.07 (0.04)                | 87.40 (0.02)        | 90.79                               | 78.52                               |

## Data sources

The table below shows the data sources used to train the pipelines. Note that the Ugnayan treebank is not licensed for commercial use while TLUnified is under GNU GPL. Please consider these licenses when using the calamanCy pipelines in your application. I'd definitely want to gain access to commercial-friendly datasets (or develop my own). If you have any leads or just wanna help out, feel free to contact me by e-mail ([ljvmiranda at gmail dot com](mailto:ljvmiranda@gmail.com))!

| Source                                                                                  | Authors                                          | License         |
| --------------------------------------------------------------------------------------- | ------------------------------------------------ | --------------- |
| [TLUnified Dataset](https://aclanthology.org/2022.lrec-1.703/)                          | Jan Christian Blaise Cruz and Charibeth Cheng    | GNU GPL 3.0     |
| [UD_Tagalog-TRG](https://universaldependencies.org/treebanks/tl_trg/index.html)         | Stephanie Samson, Daniel Zeman, and Mary Ann Tan | CC BY-SA 3.0    |
| [UD_Tagalog-Ugnayan](https://universaldependencies.org/treebanks/tl_ugnayan/index.html) | Angelina Aquino                                  | CC BY-NC_SA 4.0 |

## Next steps

For the past few months, I found two annotators and did a small annotation project to re-annotate TLUnified. I learned a lot about this process and I'll be sharing my learnings in a blog post _very_ soon. In the medium-term, I want to re-annotate TLUnified again with more fine-grained entity types and perhaps create our own treebank.

I am still in the process of testing these models so expect a few more patch releases in the future. I'm quite ahead of my self-imposed August deadline, but I want to release early and often so here it goes. If you found any issues, feel free to post them in the [Issue tracker](https://github.com/ljvmiranda921/calamanCy/issues).
