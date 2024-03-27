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

2. Black-box approach
    - Directly use the audio excerpt as input to the model
    - Let the model learn the accent classification on its own