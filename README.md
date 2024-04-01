# Accent Localizer
A Machine learning project to classify English accents based on audio excerpts.

## Introduction

The project uses the Mozilla Common Voice dataset.
The dataset contains audio excerpts of people reading out random sentences in English.
The model is trained on the audio excerpts and curated accent labels.
The model is then used to predict the accent of a speaker based on an audio excerpt.

## Implementation Strategies

Currently, two strategies are being considered for the implementation of the project.

1. Phoneme-based audio classification
    - Extract phonemes from the audio excerpt using allosaurus
    - Use the phonemes to classify the accent

Update: It seems that allosaurus only accepts wav-based inputs.
Converting millions of mp3 files to wav is not feasible.

2. [Luca Arrotta](https://github.com/lucaArrotta/Age-Estimation-based-on-Human-Voice)'s approach
    - Use a spectrogram of the audio excerpt as input to the model
    - Let the model learn the accent classification using its features

## Supported Region Codes

US: Generic American / Mid-Atlantic
CAN: Generic Canadian (Except Quebec)
CAB: Carribean (Except Creoles)
HIS: Latino / Romance (Except French)

EU: Generic European (Unspecified)
ENG: England English
CEL: Irish / Scottish / Welsh
FR: French / Quebec / Creoles
GER: Germanic Languages
EAU: Eastern European / Slavic

ME: Middle Eastern and North African
WAF: West African
ZA: South African
EAF: East African

ETA: East Asian (Mandarin / Cantonese, Japanese, Korean etc.)
IN: Indian (Indian, Pakistani, Bangladeshi etc.)
SEA: South-East Asian (Vietnamese, Thai, Malaysian, Indonesian, Filipino etc.)
NEA: Turkish / Persian / Central Asian (Near East Asian)

AUS: Australian
NZ: New Zealander / Pacific Islander