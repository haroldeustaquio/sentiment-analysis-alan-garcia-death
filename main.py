import json
import pandas as pd
import logging
from src.text_processing import TextCleaner, EmojiConversion, SentimentAnalysis

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clean_df():
    # Cargar datos
    logger.info("Loading datasets...")
    df_1 = pd.read_csv('./data/original/db_AGP_2019_sucesos.csv')
    df_2 = pd.read_csv('./data/original/postID_suceso.csv')
    
    # Merge
    logger.info("Merging datasets...")
    df = df_1.merge(df_2, how='inner', left_on='id', right_on='POST NRO')
    
    # Limpiar
    logger.info("Cleaning dataset...")
    df = df.drop(columns=['created_time.1', 'created_time.2', 'POST NRO', 'id'])
    df.columns = ['post', 'comment', 'datetime', 'context']
    
    # Borrar duplicados
    logger.info("Removing duplicates...")
    df = df.drop_duplicates()
    
    # Reset index
    logger.info("Resetting index...")
    df = df.reset_index(drop=True)
    
    # Save cleaned dataset
    logger.info("Saving cleaned dataset...")
    df.to_csv('./data/processed/data_cleaned.csv', index=False)


def clean_analyze_text():
    logger.info("Loading dataset...")
    df = pd.read_csv('./data/processed/data_cleaned.csv')
    
    logger.info("Cleaning text data...")
    cleaner = TextCleaner(df['comment'])
    cleaner.to_lowercase()
    cleaner.remove_unwanted_chars()
    cleaner.remove_url()
    cleaner.remove_punctuation()
    cleaner.remove_stop_words()
    cleaner.to_strip()
    df['comment'] = cleaner.get_cleaned_text()

    logger.info("Replacing emojis with interpretations...")
    with open('./data/emojis_interpretation.json', 'r', encoding='utf-8') as f:
        emojis_dict = json.load(f)
    emojconv = EmojiConversion(emojis_dict, df['comment'])
    emojconv.replace_emoji()
    df['comment'] = emojconv.get_text()
    df = df[df['comment'].str.split().str.len()!=0].reset_index(drop=True)
    
    logger.info("Performing sentiment analysis...")
    lexicon = pd.read_csv('./data/espaniol_NRC.csv', index_col='Spanish Word')
    lexicon.drop(columns=['anticipacion','positivo','confianza','negativo'], inplace=True)

    sentiment_analyzer = SentimentAnalysis(lexicon, df['comment'])
    sentiment_analyzer.process_feelings()
    df['feelings'] = sentiment_analyzer.get_feelings()
    
    logger.info("Saving cleaned text data...")
    df.to_csv('./data/processed/data_with_feelings.csv', index=False, encoding='utf-8')

def main():
    clean_df()
    clean_analyze_text()

if __name__ == "__main__":
    main()