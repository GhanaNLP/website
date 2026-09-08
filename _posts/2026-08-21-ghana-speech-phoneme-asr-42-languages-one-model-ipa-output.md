---
layout: post
title: "ghana-speech-phoneme-asr: 42 Languages, One Model, IPA Output"
date: 2026-08-21T16:00:00Z
categories:
  - tech
author_name: "GhanaNLP"
tags: [speech-recognition, african-languages, phoneme, ipa, machine-learning, ghana]
---

## Introduction

Most ASR models output words. This one outputs **phonemes** — the actual sounds of speech in IPA (International Phonetic Alphabet). Introducing **ghana-speech-phoneme-asr**: a single model that transcribes speech from **42 Ghanaian languages** directly into IPA phonemes.

## What It Does

Instead of producing text like "akwaaba", it produces the phonetic sequence `a k w a a b a`. This is useful for forced alignment, pronunciation analysis, TTS front-ends, and cross-language comparison.

The model has **316 million parameters** and outputs **172 IPA phoneme units** plus punctuation. It was trained on **2,329 hours** of audio from our [ghana-speech](https://huggingface.co/datasets/ghananlpcommunity/ghana-speech) dataset.

## How It Works

We fine-tuned Facebook's **omniASR_W2V_300M** encoder with a CTC head trained from scratch. Training ran on a single H200 GPU with temperature sampling across languages, so low-resource languages aren't drowned out by high-resource ones.

Phoneme targets came from **ghana-g2p**, our grapheme-to-phoneme toolkit. Multi-character IPA symbols like `kʰ` and `t͡ʃ` were mapped to single tokens during training, then mapped back to real IPA in the output.

## Results

The model achieves **16.64% UER** (Unit Error Rate) overall, or **15.39%** excluding punctuation. Performance varies by language — Selee scores 5.6% while some languages with inconsistent phoneme rules score higher.

## Quick Start

```python
import sherpa_onnx, soundfile as sf

rec = sherpa_onnx.OfflineRecognizer.from_omnilingual_asr_ctc(
    model="onnx/model.int8.onnx",
    tokens="onnx/tokens.txt",
)

wav, sr = sf.read("utterance.wav", dtype="float32")
s = rec.create_stream()
s.accept_waveform(sr, wav)
rec.decode_stream(s)
print(s.result.tokens)  # ['a', 'k', 'w', 'a', 'a', 'b', 'a']
```

## Why This Matters

**For TTS:** Get phoneme-aligned audio without manual annotation. Feed the output directly into a TTS training pipeline.

**For Linguists:** Study pronunciation patterns across 42 languages using a consistent phoneme framework.

**For Developers:** The ONNX model runs on mobile via sherpa-onnx — no GPU required.

## Quick Links

- **Model**: [ghananlpcommunity/ghana-speech-phoneme-asr](https://huggingface.co/ghananlpcommunity/ghana-speech-phoneme-asr)
- **Training Code**: [GhanaNLP/ghana-phoneme-asr](https://github.com/GhanaNLP/ghana-phoneme-asr)
- **G2P Toolkit**: [GhanaNLP/ghana-g2p](https://github.com/GhanaNLP/ghana-g2p)
- **Join Us**: [Ghana NLP Community](https://forms.gle/KVySBwS67awkRRxz5)