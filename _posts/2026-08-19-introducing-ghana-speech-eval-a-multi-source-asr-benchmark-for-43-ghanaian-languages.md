---
title: "Introducing ghana-speech-eval: A Multi-Source ASR Benchmark for 43
  Ghanaian Languages"
date: 2026-08-19T13:41:54.474Z
categories:
  - ASR
tags:
  - speech-recognition
  - african-languages
  - machine-learning
  - evaluation
  - ghana
author_name: GhanaNLP
---
<h5>Introduction</h5>

<p>Building speech recognition for Ghanaian languages is hard. But knowing whether your model actually works? That's even harder.</p>

<p>There are plenty of ASR (Automatic Speech Recognition) models out there — Whisper, MMS, Wav2Vec2 — and some claim to support African languages. But when you dig deeper, you find that most evaluations are either done on English data, or on a handful of "major" languages like Swahili or Amharic. Very few benchmarks exist for Ghanaian languages specifically, and even fewer cover the full diversity of languages spoken in Ghana.</p>

<p>That's why we built <b>ghana-speech-eval</b> — a comprehensive evaluation benchmark for measuring ASR quality across <b>43 Ghanaian languages</b>, with over <b>61,000 audio clips</b> from multiple sources.</p>

<p>
<div class="">
    <img src="{{'/assets/img/blog/ghana-speech-eval-overview.png' | relative_url }}" alt="ghana-speech-eval overview">
</div>
<b>Fig. 1:</b> Overview of the ghana-speech-eval dataset — 65 subsets across 43 Ghanaian languages
</p>

<h5>What's Inside the Dataset</h5>

<p>The dataset is organized into <b>65 subsets</b> across six different source groups:</p>

<p>
<div class="">
    <img src="{{'/assets/img/blog/ghana-speech-eval-sources.png' | relative_url }}" alt="data sources">
</div>
<b>Fig. 2:</b> Source groups and their contributions to the dataset
</p>

<p>Each source gives us different types of speech — Bible readings, finance-domain conversations, health recordings, and more. This diversity matters because a model that works well on read speech might struggle with conversational audio, and vice versa.</p>

<p>Here's what each source brings:</p>

<p>- <b>Bible audio</b> (42 languages): Clean, read speech with verified transcriptions. This is our largest source, covering almost every Ghanaian language we could find recordings for.</p>

<p>- <b>Finance-domain speech</b> (4 languages): Multi-speaker conversations about financial topics. This tests how well models handle domain-specific vocabulary.</p>

<p>- <b>JW.org speech</b> (9 languages): Another source of read speech, but from a different organization with different recording conditions.</p>

<p>- <b>LDS conference speech</b> (2 languages): Formal speech from religious conferences, giving us a different speaking style to test against.</p>

<p>- <b>UNICEF health recordings</b> (3 languages): Health-related speech that's particularly useful for building real-world applications like health chatbots.</p>

<p>- <b>WaxalNLP ASR data</b> (5 languages): Additional data from Google's WaxalNLP project, adding more diversity to our evaluation set.</p>

<h5>Languages Covered</h5>

<p>We cover <b>43 Ghanaian languages</b>, including major languages like Twi (both Akuapem and Asante dialects), Ewe, Fante, Ga, Dagbani, and Hausa, as well as lesser-studied languages like Kasem, Buli, Bassar Ntcham, Avatime, and Siwu.</p>

<p>One important decision we made was to treat <b>Akuapem Twi</b> and <b>Asante Twi</b> as separate languages. While they're both called "Twi" and share the same ISO code, they have different orthographies and can sound quite different. Previously, when these were merged, we found that models would score well on one dialect but poorly on the other — giving misleading overall results.</p>

<p>By keeping them separate, you can now see exactly how your model performs on each dialect.</p>

<h5>How We Built It</h5>

<p>The dataset was built using <b>speecheval-builder</b>, our open-source toolkit for creating speech evaluation datasets. The process involved:</p>

<p><b>1. Audio Collection:</b> We gathered audio from multiple sources, each chosen to represent different speaking styles and recording conditions.</p>

<p><b>2. Text Alignment:</b> For each audio clip, we aligned it with the corresponding text transcription. This is crucial — without accurate text, you can't measure ASR quality.</p>

<p><b>3. Quality Control:</b> We filtered out clips that were too short, too noisy, or had unclear transcriptions.</p>

<p><b>4. Standardization:</b> All clips were converted to 16 kHz mono audio with a standardized schema, making it easy to use with any ASR framework.</p>

<p><b>5. Language Verification:</b> We double-checked language labels and dialect classifications, especially for closely related languages.</p>

<p>
<div class="">
    <img src="{{'/assets/img/blog/ghana-speech-eval-pipeline.png' | relative_url }}" alt="pipeline">
</div>
<b>Fig. 3:</b> The speecheval-builder pipeline used to create the dataset
</p>

<h5>Why This Matters</h5>

<p><b>For Researchers:</b> If you're working on ASR for Ghanaian languages, this dataset gives you a fair, consistent way to compare your model against others. No more cherry-picking test sentences or reporting results on easy subsets. Every language has the same evaluation protocol, with the same number of samples.</p>

<p><b>For Developers:</b> Building an app that needs to recognize Twi, Ewe, or Dagbani speech? Use this benchmark to figure out which existing model works best for your use case. Our interactive leaderboard at nsanku-asr-benchmark shows WER (Word Error Rate) and CER (Character Error Rate) for multiple models across all 43 languages.</p>

<p><b>For the Community:</b> This dataset is open source (CC-BY-4.0 license) and hosted on Hugging Face, making it easy for anyone to use. We want this to become the standard way we evaluate speech recognition progress for Ghanaian languages.</p>

<h5>Getting Started</h5>

<p>Loading the dataset is simple:</p>

<pre><code>from datasets import load_dataset

# Load Twi (Asante) evaluation data
ds = load_dataset("ghananlpcommunity/ghana-speech-eval", "bible_Asante_Twi", split="eval")

# See what's in it
print(ds[0])
# {'audio': &lt;audio&gt;, 'text': '...', 'language': 'Asante Twi', ...}
</code></pre>

<p>You can also explore all available configurations:</p>

<pre><code>from datasets import get_dataset_config_names

configs = get_dataset_config_names("ghananlpcommunity/ghana-speech-eval")
print(f"Total subsets: {len(configs)}")
# Output: Total subsets: 65
</code></pre>

<h5>What's Next</h5>

<p>This benchmark is already being used by <b>nsanku-ASR</b>, our ASR evaluation pipeline that benchmarks organization-owned models on Ghanaian languages. We're continuously adding more audio sources and languages.</p>

<p>If you have audio data for a Ghanaian language that isn't represented here, we'd love to hear from you! Reach out to us at info@ghananlp.org or join our community.</p>

<p>
<div class="">
    <img src="{{'/assets/img/blog/ghana-speech-eval-languages.png' | relative_url }}" alt="languages map">
</div>
<b>Fig. 4:</b> The 43 Ghanaian languages covered by ghana-speech-eval
</p>

<h5>Quick Links</h5>

<p>- <b>Dataset:</b> <a href="https://huggingface.co/datasets/ghananlpcommunity/ghana-speech-eval">ghananlpcommunity/ghana-speech-eval</a></p>
<p>- <b>Leaderboard:</b> <a href="https://huggingface.co/spaces/ghananlpcommunity/nsanku-asr-benchmark">nsanku-asr-benchmark</a></p>
<p>- <b>Builder Toolkit:</b> <a href="https://github.com/GhanaNLP/speecheval-builder">GhanaNLP/speecheval-builder</a></p>
<p>- <b>Join Us:</b> <a href="https://forms.gle/KVySBwS67awkRRxz5">Ghana NLP Community</a></p>