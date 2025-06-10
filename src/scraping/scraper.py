from google_play_scraper import Sort, reviews_all
import pandas as pd
from datetime import datetime

# Define app package names for each bank on Google Play
apps = {
    "CBE": "com.cbe.mobilebanking",          # Replace with actual package name
    "BOA": "com.bankofabyssinia.mobile",    # Replace with actual package name
    "Dashen": "com.dashenbank.mobile"       # Replace with actual package name
}

def scrape_reviews(app_package, bank_name):
    print(f"Scraping reviews for {bank_name}...")
    all_reviews = reviews_all(
        app_package,
        sleep_milliseconds=0,  # no sleep for faster scraping (adjust if needed)
        lang='en',             # language filter (optional)
        country='us',          # country filter (optional)
        sort=Sort.NEWEST       # sort by newest first
    )
    # Extract needed fields only
    reviews_data = []
    for r in all_reviews:
        reviews_data.append({
            "review": r["content"],
            "rating": r["score"],
            "date": r["at"].strftime("%Y-%m-%d"),
            "bank": bank_name,
            "source": "Google Play"
        })
    print(f"Total reviews scraped for {bank_name}: {len(reviews_data)}")
    return reviews_data

def main():
    all_banks_reviews = []

    for bank, pkg in apps.items():
        bank_reviews = scrape_reviews(pkg, bank)
        # Limit to 400 reviews per bank (if more scraped)
        bank_reviews = bank_reviews[:400]
        all_banks_reviews.extend(bank_reviews)

    # Convert to DataFrame and save as CSV
    df = pd.DataFrame(all_banks_reviews)
    df.to_csv("raw_reviews.csv", index=False)
    print("Saved raw reviews to raw_reviews.csv")

if __name__ == "__main__":
    main()
