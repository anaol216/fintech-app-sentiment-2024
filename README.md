Here is a comprehensive `README.md` file that a new developer can use to understand and run the project from scratch. It covers everything we did, from setting up the database to deriving the final insights.

-----

# Bank Reviews Analysis and Sentiment Analysis Project

## 📜 Project Overview

This project is a data science pipeline that collects, cleans, and analyzes customer reviews from bank mobile applications. The goal is to derive actionable insights, identify key user pain points and drivers of positive feedback, and provide data-driven recommendations for app improvement. The entire pipeline is designed to be reproducible and is built using Python, pandas, and a PostgreSQL database.

## 🛠️ Technology Stack

  * **Python 3.x:** Core programming language.
  * **Pandas:** For data manipulation and cleaning.
  * **NLTK & Scikit-learn:** For text preprocessing, sentiment analysis, and theme identification.
  * **PostgreSQL:** A relational database used for data persistence.
  * **`psycopg2`:** The Python adapter for PostgreSQL.
  * **Matplotlib & Seaborn:** For data visualization.
  * **Jupyter Notebook:** For a step-by-step, interactive development environment.

## 📁 Project Structure

```
.
├── data/
│   ├── processed/
│   │   └── analyzed_reviews.csv
│   └── raw/
│       └── <raw_data_files>
├── notebooks/
│   ├── data_collection.ipynb
│   ├── data_cleaning.ipynb
│   ├── db_loading.ipynb
│   └──insights.ipynb
├── src/
│   └── db_loader.py
│   ├── analyzer.py
│   ├── scraper.py
│   └──preprocess.py
├── .gitignore
├── README.md
└── requirements.txt
```

## 🚀 Setup and Installation

### **1. Clone the Repository**

```bash
git clone https://github.com/anaol216/fintech-app-sentiment-2024.git
cd bank_reviews_analysis
```

### **2. Set up the Python Environment**

It's recommended to use a virtual environment.

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
.\venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

# Install the required Python packages
pip install pandas psycopg2-binary matplotlib seaborn jupyter
```

### **3. Set up the PostgreSQL Database**

This project uses PostgreSQL for data storage.

1.  **Install PostgreSQL:** Download and install PostgreSQL from the official website. The installer typically includes **`pgAdmin`**, a useful graphical tool for managing your database.
2.  **Create a User and Database:** Use `pgAdmin` to create a new database. We will call it `banks_statements`. You should also remember the password for the default `postgres` user.
3.  **Configure Authentication:** If you encounter a `"password authentication failed"` error, you may need to configure the `pg_hba.conf` file to allow local connections without a password.
      * Find the file (e.g., `C:\Program Files\PostgreSQL\16\data\pg_hba.conf`).
      * Change the authentication method for `127.0.0.1` and `::1` from `scram-sha-256` to **`trust`**.
      * Restart the PostgreSQL service.

### **4. Configure Environment Variable**

The project connects to the database using an environment variable for security. Before running the notebook, set your PostgreSQL password in the terminal:

  * **For Windows (Command Prompt):**
    ```cmd
    set DB_PASSWORD=your_postgres_password
    ```
  * **For macOS/Linux (Terminal):**
    ```bash
    export DB_PASSWORD=your_postgres_password
    ```

## 🏃 Execution

Navigate to the `notebooks` directory and open the notebooks in order.

### **Task 1: Data Collection & Cleaning**

The first notebook handles data loading and initial cleaning.

### **Task 2: Analysis**

This notebook performs sentiment analysis and identifies key themes.

### **Task 3: Database Loading**

This notebook loads the cleaned and analyzed data into the PostgreSQL database. It uses `src/db_loader.py` for database connection and data loading logic.

### **Task 4: Insights and Recommendations**

This final notebook retrieves the data from the database, visualizes the key findings, and presents a final analysis and recommendations.

## 📈 Key Findings and Recommendations

Based on the analysis, here are the key insights and recommendations:

### **Insights**

  * **Sentiment vs. Rating:** A strong positive correlation exists between high ratings and positive sentiment, and low ratings and negative sentiment . This indicates that the sentiment analysis model is effective in capturing user satisfaction.
  * **Dominant Pain Points:** "Transaction Performance" is a major pain point mentioned across multiple banks. The most frequent negative theme is "Other," suggesting a wide range of unique issues that need to be addressed on a case-by-case basis.
  * **Overall Sentiment:** The majority of reviews are positive, with more than 700 positive reviews compared to roughly 450 negative ones.

### **Recommendations**

1.  **Prioritize Transaction Performance:** Since "Transaction Performance" is a top pain point, a key recommendation is to optimize the speed and reliability of transactions. This will directly address a major source of user frustration.
2.  **Improve User Interface:** The analysis of themes like "User Interface & Experience" suggests that a redesign to create a more intuitive and stable app could significantly improve user satisfaction.
3.  **Analyze "Other" Feedback:** Since "Other" is a dominant category for both drivers and pain points, further qualitative analysis on the raw review text is needed to uncover new, recurring themes that were not captured by the initial model.

-----

**Author:** Anaol A.
**Date:** August 21/2025