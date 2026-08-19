---
title: "Introducing ghana-speech: 2,247 Hours of Speech Data for 42 Ghanaian
  Languages"
date: 2026-08-19T14:08:03.529Z
post_image: /assets/img/uploads/b2.jpg
categories:
  - tech
tags:
  - speech-recognition
  - african-languages
  - dataset
  - machine-learning
  - ghana
author_name: GhanaNLP
---
## Introduction

Building speech recognition for Ghanaian languages starts with one thing: data. Today we're introducing **ghana-speech** — a dataset with **1,411,467 audio segments** totaling **2,247 hours** across **42 Ghanaian languages**.

This isn't a small experimental dataset. This is the scale needed to train real, production-quality ASR systems.

## What's Inside

The dataset covers 42 languages with varying amounts of audio. Here are the top languages by hours:

| Language | Hours |
|----------|-------|
| Asante Twi | 200h |
| Ewe | 161h |
| Hausa | 153h |
| Fante | 122h |
| Kasem | 98h |
| Lelemi | 94h |
| Bimoba | 91h |
| Gonja | 86h |
| Buli | 86h |
| Sisaala Tumulung | 82h |

Every language has at least 3 hours of audio, with most having 15+ hours.

## How We Built It

The backbone is Bible audio recordings. Why Bible data? Because every clip has a verified text transcription, the recordings are clean professional audio, and Bible translations exist for almost every Ghanaian language.

We supplemented this with other sources to add speaking style diversity.

## Why This Matters

**For ASR Development:** Previous efforts had tens or hundreds of hours. With 2,247 hours, you can now train serious models that work in real-world conditions.

**For Transfer Learning:** Train on a well-resourced language like Twi, then fine-tune on a lower-resource language. Acoustic patterns transfer well across related languages.

**For Everyone:** This dataset is open source (CC-BY-NC-4.0) on Hugging Face. No paywalls, no restrictions.

## Getting Started

```python
from datasets import load_dataset

ds = load_dataset("ghananlpcommunity/ghana-speech", "Asante_Twi_twi", split="train")
print(ds[0])
```

## Quick Links

- **Dataset**: [ghananlpcommunity/ghana-speech](https://huggingface.co/datasets/ghananlpcommunity/ghana-speech)
- **Join Us**: [Ghana NLP Community](https://forms.gle/KVySBwS67awkRRxz5)