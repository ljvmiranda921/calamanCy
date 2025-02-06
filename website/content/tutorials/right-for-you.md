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

## Level 0: Use off-the-shelf calamanCy models

The very first step is to try the [off-the-shelf calamanCy models](https://huggingface.co/collections/ljvmiranda921/calamancy-models-for-tagalog-nlp-65629cc46ef2a1d0f9605c87) and see if they give you decent performance.
As of writing (v0.2.0), the NER models only handle PER (person), ORG (organization), and LOC (location) entities, so if you need more than that then you have to move to the next step!

- **Cost (0 &rarr; 💰):** almost no cost to try out the medium and large models. You might need a small GPU to use the transformer-based model (I can run it reliably on an NVIDIA RTX 3060 gaming laptop).
- **Involvement (💪):** almost no involvement at all! You just need to run the text on a calamanCy model and off you go!

## Level 1: Can spacy-llm or my GliNER finetunes handle it?

Using my GliNER finetunes on Tagalog is useful if you need to detect entities other than PER, ORG, and LOC.
Although I find that GliNER models perform a bit worse than a fully-finetuned model during my [internal evaluations](https://ljvmiranda921.github.io/calamanCy/news/gliner/), its flexibility is hard to match.
You can find all my GliNER finetunes [here](https://huggingface.co/ljvmiranda921/tl_gliner_large).

Another interesting project is [spacy-llm](https://github.com/explosion/spacy-llm).
It allows you to use the full gamut of an LLM's zero-shot capabilities on linguistic tasks like NER.
In my [previous paper](https://aclanthology.org/2023.sealp-1.2.pdf), I find that these LLM-based methods don't work as well in Tagalog, but that was 2023&mdash; way before multilingual LLMs have taken full form.

## Level 2: Finetune your own model!
