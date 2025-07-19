# Sentiment Analysis - Alan García Death

## Overview

This project analyzes public sentiment regarding the death of former Peruvian President Alan García through social media comments. The analysis focuses on Facebook comments collected during key events surrounding his death in April 2019, applying natural language processing techniques to classify emotional responses and understand public opinion.

## Content

- [Data](#data)
- [Notebooks](#notebooks) 
- [Source Code](#src)
- [Main Script](#main-script)

---

## Data

### `data/original/`
Contains the raw datasets:
- `db_AGP_2019_sucesos.csv` - Original comments with timestamps and metadata
- `postID_suceso.csv` - Post IDs mapped to specific events/contexts

### `data/processed/`
Contains cleaned and processed datasets:
- `data_cleaned.csv` - Merged and cleaned comments with proper formatting
- `data_with_feelings.csv` - Final dataset with sentiment classifications added

### `data/`
- `espaniol_NRC.csv` - Spanish emotion lexicon used for sentiment analysis

---

## Notebooks

### [`01_df_cleaning.ipynb`](notebooks/01_df_cleaning.ipynb)
Data preparation and cleaning pipeline:
- Merges multiple data sources
- Removes duplicates and irrelevant columns
- Standardizes column names and formats
- Exports cleaned dataset

### [`02_sentiment_analysis.ipynb`](notebooks/02_sentiment_analysis.ipynb)
Sentiment analysis implementation:
- Text preprocessing and cleaning
- Emoji interpretation and conversion
- Sentiment classification using Spanish NRC lexicon
- Emotion categorization (alegría, ira, neutral, sorpresa, etc.)
- Final dataset export with sentiment labels

---

## Src

Contains the core text processing modules:
- Text cleaning utilities
- Preprocessing functions for Spanish text
- Emoji handling and interpretation
- Sentiment analysis implementation

---

## Main Script

[`main.py`](main.py) - Central execution script that orchestrates the entire pipeline:
- Data loading and merging
- Dataset cleaning and preparation
- Automated processing workflow
- Logging and error handling

The script provides a streamlined way to execute the complete analysis pipeline from raw data to final sentiment