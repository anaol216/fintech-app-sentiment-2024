# src/preprocessor.py

import pandas as pd

def preprocess_data(df):
    """
    Cleans and preprocesses the raw review data.
    
    Args:
        df (pd.DataFrame): The raw DataFrame from scraping.
        
    Returns:
        pd.DataFrame: The cleaned and preprocessed DataFrame.
    """
    if df.empty:
        print("DataFrame is empty. No preprocessing to perform.")
        return df

    # Select and rename relevant columns
    df = df[['content', 'score', 'at', 'bank', 'source']].copy()
    df.columns = ['review', 'rating', 'date', 'bank', 'source']
    
    # Drop rows with any missing values
    initial_rows = len(df)
    df.dropna(subset=['review', 'rating', 'date'], inplace=True)
    print(f"Dropped {initial_rows - len(df)} rows with missing data.")
    
    # Remove duplicates based on review text and date
    initial_rows_dup = len(df)
    df.drop_duplicates(subset=['review', 'date'], inplace=True)
    print(f"Dropped {initial_rows_dup - len(df)} duplicate reviews.")
    
    # Normalize dates to YYYY-MM-DD format
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
    
    print(f"Final number of reviews after preprocessing: {len(df)}")
    
    return df

def save_clean_data(df, file_path):
    """Saves the cleaned DataFrame to a CSV file."""
    if not df.empty:
        df.to_csv(file_path, index=False)
        print(f"Cleaned data saved to {file_path}")
    else:
        print("DataFrame is empty. No data to save.")