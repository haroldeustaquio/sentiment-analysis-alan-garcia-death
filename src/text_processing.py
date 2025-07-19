from string import punctuation 
import pandas as pd
from nltk.corpus import stopwords
import logging
import re


class TextCleaner:
    def __init__(self, text: pd.Series):
        self.text = text
        self.logger = logging.getLogger(__name__)
    
    def remove_punctuation(self):
        self.logger.info("Removing punctuation from text")
        try:
            self.text = self.text.str.replace(f'[{punctuation}]', '', regex=True)
            self.logger.info("Punctuation removed successfully")
        except Exception as e:
            self.logger.error(f"Error removing punctuation: {e}")

    def to_lowercase(self):
        self.logger.info("Converting text to lowercase")
        try:
            self.text = self.text.str.lower()
            self.logger.info("Text converted to lowercase successfully")
        except Exception as e:
            self.logger.error(f"Error converting text to lowercase: {e}")

    def to_strip(self):
        self.logger.info("Stripping whitespace from text")
        try:
            self.text = self.text.str.strip()
            self.logger.info("Whitespace stripped successfully")
        except Exception as e:
            self.logger.error(f"Error stripping whitespace: {e}")

    def remove_stop_words(self, language='spanish'):
        self.logger.info(f"Removing stop words from text (language: {language})")
        try:
            stop_words = set(stopwords.words(language))
            self.text = self.text.apply(
                lambda x: ' '.join(
                    word for word in str(x).split() if word.lower() not in stop_words
                ) if pd.notna(x) else x
            )
            self.logger.info("Stop words removed successfully")
        except Exception as e:
            self.logger.error(f"Error removing stop words: {e}")

    def remove_url(self):
        self.logger.info("Removing URLs from text")
        try:
            self.text = self.text.str.replace(r'http\S+|www\S+|https\S+', '', regex=True)
            self.logger.info("URLs removed successfully")
        except Exception as e:
            self.logger.error(f"Error removing URLs: {e}")

    def remove_unwanted_chars(self):
        self.logger.info("Removing unwanted characters")
        try:
            self.text = self.text.str.replace(r'\n|\t|\r', ' ', regex=True)
            self.text = self.text.str.replace(r'\s+', ' ', regex=True)
            self.logger.info("Unwanted characters removed successfully")
        except Exception as e:
            self.logger.error(f"Error removing unwanted characters: {e}")

    def get_cleaned_text(self):
        self.logger.info("Returning cleaned text")
        return self.text


class EmojiConversion:
    def __init__(self, emojis_dict, text: pd.Series):
        self.emojis_dict = emojis_dict
        self.text = text
        self.logger = logging.getLogger(__name__)
    
    def replace_emoji(self):
        self.logger.info("Replacing emojis in text")
        emoji_pattern = re.compile('|'.join(map(re.escape, self.emojis_dict.keys())))
        
        try:
            only_text = self.text.apply(lambda x: [c for c in x if c not in self.emojis_dict]).apply(lambda x: ''.join(x))
            only_emojis = self.text.apply(lambda x: re.findall(emoji_pattern, x)).apply(lambda x: ' '.join(x)).apply(lambda x: x.split()).apply(lambda x: [self.emojis_dict[emoji] for emoji in x if emoji in self.emojis_dict]).apply(lambda x: ' '.join(x))
            self.text = only_text + ' ' + only_emojis
            self.logger.info("Emojis replaced successfully")
        except Exception as e:
            self.logger.error(f"Error replacing emojis in text: {e}")

    def get_text(self):
        return self.text
    


class SentimentAnalysis:
    def __init__(self, lexicon: pd.DataFrame, text: pd.Series):
        self.lexicon= lexicon
        self.text = text
        self.feeling = 'neutral'
        self.feelings = None
        self.logger = logging.getLogger(__name__)

    def process_feelings(self):
        self.logger.info("Getting feelings from text")
        try:
            self.feelings = self.text.apply(lambda x: self._get_strong_feeling(x.split()))
            self.logger.info("Feelings calculated successfully")
        except Exception as e:
            self.logger.error(f"Error getting feelings: {e}")
            
    def _get_strong_feeling(self, words:list):
        feelings_count = {feelings: 0 for feelings in self.lexicon.columns}
        try:
            for word in words:
                if word in self.lexicon.index:
                    for feeling in self.lexicon.columns:
                        feelings_count[feeling] += self.lexicon.loc[word, feeling]
            feeling, total = sorted(feelings_count.items(), key=lambda x: x[1], reverse=True)[0]
            return feeling if total > 0 else 'neutral'
        except Exception as e:
            self.logger.error(f"Error calculating strong feeling: {e}")

    def get_feelings(self):
        self.logger.info("Returning feelings from text")
        self.process_feelings()
        return self.feelings