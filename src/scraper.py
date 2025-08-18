# src/scraper.py

import pandas as pd
from google_play_scraper import Sort, reviews

def get_all_reviews(bank_apps):
    """
    Scrapes reviews for multiple bank apps and returns a single DataFrame.
    
    Args:
        bank_apps (dict): A dictionary mapping bank names to their app IDs.
        
    Returns:
        pd.DataFrame: A DataFrame containing all scraped reviews.
    """
    all_reviews_data = []
    
    for bank_name, app_id in bank_apps.items():
        print(f"Scraping reviews for app: {bank_name} (ID: {app_id})...")
        try:
            reviews_list, _ = reviews(
                app_id,
                lang='en',
                country='et',
                sort=Sort.NEWEST,
                count=400
            )
            for review in reviews_list:
                review['bank'] = bank_name
                review['source'] = 'Google Play'
            all_reviews_data.extend(reviews_list)
        except Exception as e:
            print(f"An error occurred while scraping {bank_name}: {e}")
            
    if not all_reviews_data:
        print("No reviews were scraped. Check app IDs or network connection.")
        return pd.DataFrame()

    return pd.DataFrame(all_reviews_data)