import pandas as pd
import re

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\d+", "", text)
    return text.strip()

def preprocess_reviews(input_path="data/raw_reviews.csv", output_path="data/clean_reviews.csv"):
    df = pd.read_csv(input_path)

    # Remove duplicates
    df.drop_duplicates(subset=["reviewId", "content"], inplace=True)

    # Handle missing text
    df['content'] = df['content'].fillna("")
    df['content'] = df['content'].apply(clean_text)

    # Remove empty reviews
    df = df[df['content'].str.strip() != ""]

    # Normalize dates
    df['at'] = pd.to_datetime(df['at'], errors='coerce')
    df['at'] = df['at'].dt.strftime('%Y-%m-%d')

    # Rename and organize columns
    df.rename(columns={
        'content': 'review',
        'score': 'rating',
        'at': 'date',
        'app_name': 'bank'
    }, inplace=True)
    df['source'] = 'Google Play'

    # Final column order
    final_df = df[['review', 'rating', 'date', 'bank', 'source']]
    final_df.to_csv(output_path, index=False)
    print(f"Preprocessed reviews saved to {output_path}")

if __name__ == "__main__":
    preprocess_reviews()
