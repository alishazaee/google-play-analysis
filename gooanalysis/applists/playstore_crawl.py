from google_play_scraper import Sort, reviews
from google_play_scraper import app
from google_play_scraper import search
from dotenv import load_dotenv
from pathlib import Path
import os
from psycopg2 import sql 
import psycopg2


def fetch_reviews(app_id, count=1000):
    result, _ = reviews(
        app_id,
        lang='en', 
        country='us', 
        sort=Sort.NEWEST,  
        count=count
    )

    extracted_reviews = []
    for review in result:
        extracted_review = {
            "review_id": review['reviewId'],
            "at": review['at'],  
            "userName": review['userName'],
            "thumbsUpCount": review['thumbsUpCount'],
            "score": review['score'], 
            "content": review['content']
        }
        extracted_reviews.append(extracted_review)

    return extracted_reviews


def fetch_app_details(app_id):
   
    result = app(
        app_id,
        lang='en',  
        country='us' 
    )

    return {
        "downloads": result.get('installs', 'Unknown'),
        "score": result.get('score', 'Unknown'),
        "minInstalls": result.get('score', 'Unknown'),
        "total_reviews": result.get('reviews', 'Unknown'),
        "updated_at": result.get('updated', 'Unknown'),
        "version": result.get('version', 'Unknown'),
        "adSupported": result.get('adSupported', 'Unknown'),
        "ratings": result.get('contentRating', 'Unknown')  
    }



def DB_Connector():
    return None


def CREATE_TABLE(connector): 
    conn = connector
    # Create the Apps table
    with conn.cursor() as cur:
        cur.execute("""
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

    # Create the Reviews table
    with conn.cursor() as cur:
        cur.execute("""
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

    # Commit changes and close the connection
    conn.commit()
    conn.close()



def APP_INTO_DB(app_details, new_reviews_list ,connector):
    conn = connector
    cursor = conn.cursor()

    # Insert or Update app details
    app_data = (app_details['app_id'], app_details['downloads'], app_details['score'],
                app_details['minInstalls'], app_details['total_reviews'], app_details['updated_at'],
                app_details['version'], app_details['adSupported'], app_details['ratings'])
    
    cursor.execute('''
        INSERT INTO Apps (app_id, downloads, score, min_installs, total_reviews, updated_at, version, ad_supported, ratings)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(app_id) DO UPDATE SET
        downloads = excluded.downloads,
        score = excluded.score,
        min_installs = excluded.min_installs,
        total_reviews = excluded.total_reviews,
        updated_at = excluded.updated_at,
        version = excluded.version,
        ad_supported = excluded.ad_supported,
        ratings = excluded.ratings;
    ''', app_data)

    # Fetch existing reviews for the app
    cursor.execute('SELECT review_id, review_at, user_name, thumbs_up_count, score, content FROM Reviews WHERE app_id = ?', (app_details['app_id'],))
    existing_reviews = {row[0]: row[1:] for row in cursor.fetchall()}

    # Update or insert reviews
    for review in new_reviews_list:
        if review['review_id'] in existing_reviews:
            # Check if the review data has changed
            if existing_reviews[review['review_id']] != (review['at'], review['userName'], review['thumbsUpCount'], review['score'], review['content']):
                # Update the review
                update_data = (review['at'], review['userName'], review['thumbsUpCount'], review['score'], review['content'], review['review_id'])
                cursor.execute('''
                    UPDATE Reviews SET review_at = ?, user_name = ?, thumbs_up_count = ?, score = ?, content = ?
                    WHERE review_id = ?
                ''', update_data)
        else:
            # Insert new review
            insert_data = (review['review_id'], app_details['app_id'], review['at'], review['userName'], review['thumbsUpCount'], review['score'], review['content'])
            cursor.execute('''
                INSERT INTO Reviews (review_id, app_id, review_at, user_name, thumbs_up_count, score, content)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', insert_data)

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()
