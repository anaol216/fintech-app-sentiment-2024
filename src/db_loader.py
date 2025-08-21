# src/db_loader.py

import psycopg2
import os
import pandas as pd
from psycopg2 import sql

def get_db_connection():
    """Establishes and returns a connection to the PostgreSQL database."""
    try:
        connection = psycopg2.connect(
            host="localhost",
            database="banks_statements",
            user="postgres",
            password=os.environ.get("DB_PASSWORD")
        )
        print("Successfully connected to PostgreSQL Database.")
        return connection
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def create_tables(connection):
    """Creates the banks and reviews tables if they don't exist."""
    sql_statements = [
        """
        CREATE TABLE IF NOT EXISTS banks (
            bank_id SERIAL PRIMARY KEY,
            bank_name VARCHAR(50) UNIQUE NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS reviews (
            review_id SERIAL PRIMARY KEY,
            review_text TEXT NOT NULL,
            rating SMALLINT,
            review_date DATE,
            bank_id INTEGER,
            source VARCHAR(50),
            sentiment_label VARCHAR(20),
            sentiment_score DECIMAL(5, 4),
            identified_themes VARCHAR(255),
            CONSTRAINT fk_bank FOREIGN KEY (bank_id) REFERENCES banks(bank_id)
        )
        """
    ]

    with connection.cursor() as cursor:
        try:
            for statement in sql_statements:
                cursor.execute(statement)
            print("Tables created successfully (or already exist).")
            connection.commit()
        except psycopg2.Error as e:
            print(f"Error creating tables: {e}")
            connection.rollback()

def load_data_to_postgres(df, connection):
    """
    Loads data from the DataFrame into the PostgreSQL database.
    
    This function first loads unique banks and then the reviews, using
    the bank_id to link them.
    """
    if df.empty:
        print("DataFrame is empty. No data to load.")
        return

    try:
        with connection.cursor() as cursor:
            # First, load unique banks into the BANKS table
            banks_to_insert = df[['bank']].drop_duplicates()
            banks_sql = "INSERT INTO banks (bank_name) VALUES (%s) ON CONFLICT (bank_name) DO NOTHING"
            
            for index, row in banks_to_insert.iterrows():
                cursor.execute(banks_sql, (row['bank'],))
            connection.commit()
            
            print("Banks table populated.")

            # Get the bank_id mapping
            banks_df = pd.read_sql("SELECT bank_id, bank_name FROM banks", con=connection)
            bank_id_map = banks_df.set_index('bank_name')['bank_id'].to_dict()
            df['bank_id'] = df['bank'].map(bank_id_map)

            # Prepare data for bulk insertion into the REVIEWS table
            reviews_data = [
                (row['review'], row['rating'], row['date'], row['bank_id'], row['source'], row['sentiment_label'], row['sentiment_score'], row['identified_themes'])
                for _, row in df.iterrows()
            ]
            
            insert_reviews_sql = """
            INSERT INTO reviews (review_text, rating, review_date, bank_id, source, sentiment_label, sentiment_score, identified_themes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            cursor.executemany(insert_reviews_sql, reviews_data)
            print(f"Successfully loaded {len(df)} reviews into the database.")
            connection.commit()
            
    except psycopg2.Error as e:
        print(f"Error loading data: {e}")
        connection.rollback()