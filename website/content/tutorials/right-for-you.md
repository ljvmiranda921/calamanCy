---
title: "Is calamanCy right for you?"
date: "2025-02-05"
categories:
  - blog
---

Before we start with all the tips and tricks on how to use calamanCy, I believe it is important to first ask the question: **is calamanCy right for you?**
calamanCy may be the best fit for your use-case if you are...

- Doing **linguistic analysis and annotation** such as parts-of-speech tagging or dependency parsing.
- Looking for an **efficient and low-cost** tool for extracting information from text.

I don't think calamanCy is the best fit for you if you are **interested in more complex downstream tasks**, like search.
Back then, you do need tools like calamanCy (or spaCy) to extract named-entities as keywords and then integrating them into a semantic search workflow.
However, innovations like LLM-based [retrieval augmented generation (RAG)](https://en.wikipedia.org/wiki/Retrieval-augmented_generation)-based workflows made these processes easier to do without training or finetuning!

Although calamanCy focuses on Filipino, **modern LLMs are starting to cater to non-English languages**.
These include [Llama 3.1](https://ai.meta.com/blog/meta-llama-3-1/), [Aya Expanse](https://cohere.com/blog/aya-expanse-connecting-our-world), and [Gemma 2](https://ai.google.dev/gemma) to name a few.
I have a few thoughts on this (and the future of Filipino NLP) in another [blog post](https://ljvmiranda921.github.io/notebook/2024/12/17/filipino-llm/).

Now, if you have an NLP project and considering whether to use calamanCy or an LLM,below is a step-by-step decision guide!
I'll be **focusing mostly on named-entity recognition**, as it is the most common use-case of calamanCy.
I arranged this guide into levels, in order of my perceived difficulty and involvement.

---

## Level 1: Use off-the-shelf calamanCy models

The very first step is to try the [off-the-shelf calamanCy models](https://huggingface.co/collections/ljvmiranda921/calamancy-models-for-tagalog-nlp-65629cc46ef2a1d0f9605c87) and see if they give you decent performance.
As of writing (v0.2.0), the NER models only handle PER (person), ORG (organization), and LOC (location) entities, so if you need more than that then you have to move to the next step!

- **Cost (0 &rarr; 💰):** almost no cost to try out the medium and large models. You might need a small GPU to use the transformer-based model (I can run it reliably on an NVIDIA RTX 3060 gaming laptop).
- **Involvement (💪):** almost no involvement at all! You just need to run the text on a calamanCy model and off you go!

## Level 2: Can spacy-llm or my GliNER finetunes handle it?

Using my GliNER finetunes on Tagalog is useful if you need to detect entities other than PER, ORG, and LOC.
Although I find that GliNER models perform a bit worse than a fully-finetuned model during my [internal evaluations](https://ljvmiranda921.github.io/calamanCy/news/gliner/), its flexibility is hard to match.
You can find all my GliNER finetunes [here](https://huggingface.co/ljvmiranda921/tl_gliner_large).

Another interesting project is [spacy-llm](https://github.com/explosion/spacy-llm).
It allows you to use the full gamut of an LLM's zero-shot capabilities on linguistic tasks like NER.
In my [previous paper](https://aclanthology.org/2023.sealp-1.2.pdf), I find that these LLM-based methods don't work as well in Tagalog, but that was 2023&mdash; way before multilingual LLMs have taken full form.
My recommendation is to first use [OpenAI models like GPT-4o](https://github.com/explosion/spacy-llm/tree/main/usage_examples/ner_v3_openai), then try HuggingFace-based models like [Llama 3.1](https://github.com/explosion/spacy-llm/blob/main/spacy_llm/models/hf/openllama.py).

- **Cost (💰💰):** costs for calling API-based LLMs can definitely ballooon if you're not watching. I recommend finding a prompt template that works for you and using [OpenAI's Batch API](https://platform.openai.com/docs/guides/batch) to save costs.

  Finally, HuggingFace models require non-trivial amounts of compute.
  For example, I can do inference for an 8B model using 1 [H100 NVIDIA GPU](https://www.nvidia.com/en-us/data-center/h100/) (and at least 2 H100s for a 70B model).
  There are GPU services like [vast.ai](https://vast.ai) or [Google Colab](https://colab.google/), but your experience may vary.

- **Involvement (💪):** there's a little bit of involvement, but these are still on inference&mdash;still easy!

## Level 3: Finetune your own model!

This is the most involved level in my opinion.
Assuming you already have a high-quality dataset (no small feat!) with good inter-annotator agreement and good number of examples, then you can train your own model!

I will recommend you to follow the [same recipe](https://github.com/ljvmiranda921/calamanCy/tree/master/models/v0.2.0) I used for training calamanCy models: start with word-vector embeddings such as fastText, and then try transformer-based embeddings such as [XLM-RoBERTa](https://huggingface.co/FacebookAI/xlm-roberta-base) or [mDeBERTa-v3](https://huggingface.co/microsoft/mdeberta-v3-base).
I will be creating tutorials for these steps in the future, but for now, the recipes in the Github repository should give you a good start!

Finetuning models can be very involved as it requires compute and effort.
My advise is: **finetune models only if you're sure that off-the-shelf LLMs cannot handle your tasks.** Two years ago, there is a strong argument for finetuning models because of their cost-effectiveness, but this argument is slowly getting weaker as LLM inference becomes cheaper.

- **Cost (💰 &rarr; 💰💰):** a word-vector based model from fastText can easily be trained on a CPU. Transformer-based models can vary: I can finetune XLM-RoBERTa on a gaming laptop, but I need an A100 from a Google Colab Pro subscription to finetune an mDeBERTa-v3 model.

- **Involvement (💪💪💪):** this is the most involved, especially if you're still new to NLP! This also doesn't factor the amount of effort involved in collecting data and annotating it.
