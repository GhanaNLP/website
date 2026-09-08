---
layout: project
title: "Ghana Speech ID"
img_src: '/assets/img/project/p6.jpg'
project_name: Ghana Speech ID
project_btn: Try the demo
company: "Ghana NLP"
status: "Active"
date: 2026-08-21
app_url: 'https://huggingface.co/spaces/ghananlpcommunity/ghana-speech-id'
---

## What is Ghana Speech ID?

Ghana Speech ID tells you which language is being spoken, across **41 Ghanaian and
West African languages**. It is the piece that has to run before almost anything else:
you cannot pick the right translation model, the right speech recogniser or the right
voice until you know what language you are listening to.

## How it works

The model does not read audio directly. Speech first goes through
[Omnilingual ASR](https://github.com/facebookresearch/omnilingual-asr), which turns it
into a transcript; Ghana Speech ID then identifies the language of that text.

```
audio ──[sherpa-onnx + omniASR CTC]──▶ transcript ──[Ghana Speech ID]──▶ language
```

Splitting the work this way keeps the language identification itself tiny. The
classifier is a vocabulary lookup and one sparse gather, not a neural network doing
heavy arithmetic over audio.

## Small enough to run anywhere

The model is **8.2 MB** and runs on CPU only, in about **0.064 ms** per classification
with a 36 MB memory footprint. That is roughly four orders of magnitude cheaper than
the speech recognition running in front of it — on any device that can already run the
ASR, identifying the language is effectively free.

The inference core is C++ with a C API, so there is no Python on the device. There are
JNI and Kotlin bindings for Android, and a Swift wrapper for iOS that imports the C API
with no bridging header. The ONNX graph deliberately uses opset-13 core operators only,
so it runs in mobile onnxruntime builds.

## Give it enough audio

Accuracy depends more on how much speech you feed it than on anything else you control:

| Audio length | Accuracy |
|---|---|
| 3 seconds | 0.51 |
| 5 seconds | 0.66 |
| 7 seconds | 0.76 |
| 10 seconds | 0.78 |

**Five seconds is the practical minimum, ten gives the best result.** Past ten seconds
the curve flattens. It is also worth checking that most of the audio is actually speech
before transcribing — a recording that is half silence carries half the evidence its
duration suggests.

## What it will and will not tell you

The model is **closed-set**: it always names one of its 41 languages, including for
speech in a language it has never heard. It returns no answer at all when nothing in
the transcript gave it a basis to decide, and that case should be reported as unknown
rather than resolved to whichever language scored least badly.

The [model card](https://huggingface.co/ghananlpcommunity/ghana-speech-id) documents
how the model behaves, what it scores, and where it fails. It is worth reading before
relying on the confidence scores.

## Using it

```sh
pip install ghana-speech-id
```

```sh
ghana-speech-id "obiara na enyi nyɛden dɛ ɔbɔbɔ no nkenyan"
```

The training and evaluation scripts in the repository reproduce the model end to end,
and every release is checked for parity across scikit-learn, the Python package and the
C++ runtime.

## Quick Links

- **GitHub**: [GhanaNLP/ghana-speech-id](https://github.com/GhanaNLP/ghana-speech-id)
- **Model card**: [ghananlpcommunity/ghana-speech-id](https://huggingface.co/ghananlpcommunity/ghana-speech-id)
- **Demo**: [Try it on Hugging Face](https://huggingface.co/spaces/ghananlpcommunity/ghana-speech-id)
- **Licence**: code Apache-2.0; models and data CC BY-NC 4.0
