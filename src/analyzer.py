# src/analyzer.py

import pandas as pd
import spacy
from transformers import pipeline
import re

# Load spaCy model for text preprocessing
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading spaCy model 'en_core_web_sm'...")
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def preprocess_text_spacy(text):
    """Tokenizes, removes stop words, and lemmatizes text."""
    if not isinstance(text, str):
        return ""
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
    return " ".join(tokens)

def analyze_sentiment(df):
    """
    Analyzes sentiment using a pre-trained Hugging Face model.
    """
    sentiment_pipeline = pipeline(
        "sentiment-analysis",
        model="distilbert-base-uncased-finetuned-sst-2-english",
        return_all_scores=True
    )
    
    reviews_list = df['review'].tolist()
    batch_size = 16 
    results = []
    
    for i in range(0, len(reviews_list), batch_size):
        batch = reviews_list[i:i + batch_size]
        try:
            results.extend(sentiment_pipeline(batch))
        except Exception as e:
            print(f"Error processing batch starting at index {i}: {e}")
            results.extend([[{'label': 'neutral', 'score': 0.5}]] * len(batch))

    sentiment_labels = []
    sentiment_scores = []
    
    for item in results:
        if isinstance(item, list) and item:
            best_result = max(item, key=lambda x: x['score'])
            sentiment_labels.append(best_result['label'].lower())
            sentiment_scores.append(best_result['score'])
        else:
            sentiment_labels.append('neutral')
            sentiment_scores.append(0.5)

    df['sentiment_label'] = sentiment_labels
    df['sentiment_score'] = sentiment_scores
    
    return df

def analyze_themes(df):
    """
    Performs thematic analysis using keyword extraction and rule-based clustering.
    """
    df['cleaned_review'] = df['review'].apply(preprocess_text_spacy)

    themes = {
        'Account Access Issues': ['login', 'password', 'user name', 'access', 'fingerprint'],
        'Transaction Performance': ['slow', 'transfer', 'fast', 'transaction', 'payment'],
        'User Interface & Experience': ['ui', 'interface', 'design', 'bug', 'crash'],
        'Customer Support': ['support', 'help', 'service', 'customer care'],
        'Feature Requests': ['feature', 'add', 'option', 'loan', 'bill payment']
    }

    def assign_themes(text):
        assigned_themes = []
        for theme, keywords in themes.items():
            if any(re.search(r'\b' + keyword + r'\b', text) for keyword in keywords):
                assigned_themes.append(theme)
        return ', '.join(assigned_themes) if assigned_themes else 'Other'

    df['identified_themes'] = df['cleaned_review'].apply(assign_themes)
    df.drop(columns=['cleaned_review'], inplace=True)
    return df

def run_analysis_pipeline(df):
    """Runs the full sentiment and thematic analysis."""
    df_with_sentiment = analyze_sentiment(df)
    df_with_themes = analyze_themes(df_with_sentiment)
    
    return df_with_themes
def aggregate_data(df):
    """
    Aggregates sentiment and themes by bank and rating.
    
    Args:
        df (pd.DataFrame): The analyzed DataFrame.
    
    Returns:
        tuple: A tuple containing two DataFrames: aggregated sentiment and aggregated themes.
    """
    print("Aggregating data...")
    # Map sentiment labels to numerical values for easier aggregation
    sentiment_mapping = {'positive': 1, 'negative': -1, 'neutral': 0}
    df['sentiment_value'] = df['sentiment_label'].map(sentiment_mapping)
    
    # Aggregate sentiment by bank and rating
    sentiment_agg = df.groupby(['bank', 'rating'])['sentiment_value'].mean().reset_index()
    sentiment_agg.rename(columns={'sentiment_value': 'mean_sentiment'}, inplace=True)
    
    # Aggregate themes by bank and count
    theme_agg = df.groupby('bank')['identified_themes'].value_counts().reset_index()
    theme_agg.columns = ['bank', 'theme', 'count']
    
    return sentiment_agg, theme_agg