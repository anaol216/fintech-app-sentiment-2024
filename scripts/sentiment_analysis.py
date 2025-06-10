# scripts/sentiment_analysis.py

import pandas as pd
from utils import preprocess, get_sentiment_tb, assign_themes

# Load reviews
df = pd.read_csv("data/raw_reviews_cbe.csv")
df = df.dropna(subset=["content"]).drop_duplicates(subset=["content"])

# Apply NLP pipeline
print("⏳ Preprocessing...")
df["clean_text"] = df["content"].apply(preprocess)

print("🔍 Performing sentiment analysis...")
df["sentiment_label"] = df["content"].apply(get_sentiment_tb)

print("🧵 Assigning themes...")
df["themes"] = df["clean_text"].apply(assign_themes)

# Save output
df[["reviewId", "content", "sentiment_label", "themes"]].to_csv("data/processed_reviews_cbe.csv", index=False)
print("Done! Output saved to data/processed_reviews_cbe.csv")
