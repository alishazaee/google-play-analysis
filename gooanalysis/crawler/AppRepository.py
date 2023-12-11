from google_play_scraper import Sort, reviews
from google_play_scraper import app
from google_play_scraper import search
from dotenv import load_dotenv
from pathlib import Path
import os
from psycopg2 import sql 
import psycopg2
from datetime import datetime
from .crawler import fetch_app_details,fetch_reviews
class AppRepository:
    def __init__(self, connector):
        self.connector = connector

    def create_table(self):
        with self.connector.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Apps (
                    app_id VARCHAR(255) PRIMARY KEY,
                    downloads VARCHAR(255),
                    score REAL,
                    minInstalls INT,
                    total_reviews INT,
                    updated_at TIMESTAMP,
                    version VARCHAR(255),
                    adSupported BOOLEAN,
                    ratings VARCHAR(255)
                );
            """)
            self.connector.commit()

    def insert_or_update_app(self, app_details):
        with self.connector.cursor() as cursor:
            cursor.execute("""
                INSERT INTO Apps (app_id, downloads, score, mininstalls, total_reviews, updated_at, version, adsupported, ratings)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (app_id) DO UPDATE SET
                downloads = EXCLUDED.downloads,
                score = EXCLUDED.score,
                mininstalls = EXCLUDED.minInstalls,
                total_reviews = EXCLUDED.total_reviews,
                updated_at = EXCLUDED.updated_at,
                version = EXCLUDED.version,
                adsupported = EXCLUDED.adSupported,
                ratings = EXCLUDED.ratings;
            """, (app_details['app_id'], app_details['downloads'], app_details['score'],
                  app_details['minInstalls'], app_details['total_reviews'], app_details['updated_at'],
                  app_details['version'], app_details['adSupported'], app_details['ratings']))
            self.connector.commit()


class ReviewRepository:
    def __init__(self, connector):
        self.connector = connector

    def create_table(self):
        with self.connector.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Reviews (
                    review_id VARCHAR(255) PRIMARY KEY,
                    app_id VARCHAR(255) NOT NULL,
                    review_date TIMESTAMP,
                    userName VARCHAR(255),
                    thumbsUpCount INT,
                    score INT,
                    content TEXT,
                    FOREIGN KEY (app_id) REFERENCES Apps(app_id)
                );
            """)
            self.connector.commit()

    def insert_or_update_reviews(self, app_id, new_reviews_list):
        conn = self.connector
        cursor = conn.cursor()
        new_review_ids = {review['review_id'] for review in new_reviews_list}

        cursor.execute("SELECT review_id, review_date, username, thumbsupcount, score, content FROM Reviews WHERE app_id = %s", (app_id,))
        existing_reviews = {row[0]: row[1:] for row in cursor.fetchall()}

    # Fetch existing reviews for the app
        cursor.execute("SELECT review_id, review_date, username, thumbsupcount, score, content FROM Reviews WHERE app_id = %s", (app_id,))
        existing_reviews = {row[0]: row[1:] for row in cursor.fetchall()}

        # Update or insert new reviews and check for content changes
        for review in new_reviews_list:
            existing_review_data = existing_reviews.get(review['review_id'])

            # Check if the review exists and if the content has changed
            if existing_review_data:
                if existing_review_data[-1] != review['content']:  # Comparing the content field
                    # Update the review as the content has changed
                    update_data = (review['at'], review['userName'], review['thumbsUpCount'], review['score'], review['content'], review['review_id'])
                    cursor.execute('''
                        UPDATE Reviews SET review_date = %s, username = %s, thumbsupcount = %s, score = %s, content = %s
                        WHERE review_id = %s
                    ''', update_data)
            else:
                # Insert new review
                insert_data = (review['review_id'], app_id, review['at'], review['userName'], review['thumbsUpCount'], review['score'], review['content'])
                cursor.execute('''
                    INSERT INTO Reviews (review_id, app_id, review_date, username, thumbsupcount, score, content) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                ''', insert_data)

        # Delete reviews that are not in the new reviews list
        reviews_to_delete = existing_reviews.keys() - new_review_ids
        for review_id in reviews_to_delete:
            cursor.execute("DELETE FROM Reviews WHERE review_id = %s", (review_id,))

        conn.commit()
 


def DB_Connector():
    conn = psycopg2.connect(
        dbname="gooanalysis",
        user="user",
        password="password",
        host="127.0.0.1",
        port="5432"
    )    

    return conn


def APP_INTO_DB(app_id):
    connector = DB_Connector()
    
    app_repo = AppRepository(connector)
    review_repo = ReviewRepository(connector)

    app_repo.create_table()
    review_repo.create_table()

    app_details = fetch_app_details(app_id=app_id)
    new_reviews_list = fetch_reviews(app_id=app_id)
    
    app_repo.insert_or_update_app(app_details)
    review_repo.insert_or_update_reviews(app_id=app_id, new_reviews_list=new_reviews_list)

    connector.close()