from google_play_scraper import Sort, reviews
from google_play_scraper import app
from google_play_scraper import search
from dotenv import load_dotenv
from pathlib import Path
import os
from psycopg2 import sql 
import psycopg2
from datetime import datetime


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
        "updated_at": str(datetime.fromtimestamp((result.get('updated')))),
        "version": result.get('version', 'Unknown'),
        "adSupported": result.get('adSupported', 'Unknown'),
        "ratings": result.get('contentRating', 'Unknown'),
        "app_id": app_id
    }



def DB_Connector():
    conn = psycopg2.connect(
        dbname="gooanalysis",
        user="user",
        password="password",
        host="127.0.0.1",
        port="5432"
    )

    # Creating a cursor object using the cursor() method
    

    return conn

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


def APP_INTO_DB():
    connector = DB_Connector()
    CREATE_TABLE(connector=connector)
    connector = DB_Connector()
    APP_DETAIL_UPDATE(app_details = fetch_app_details(app_id="com.instagram.android") , new_reviews_list=fetch_reviews(app_id="com.instagram.android"),connector=connector)



def APP_DETAIL_UPDATE(app_details, new_reviews_list ,connector):
    conn = connector
    cursor = conn.cursor()

    # Insert or Update app details
    app_data = (app_details['app_id'], app_details['downloads'], app_details['score'],
                app_details['minInstalls'], app_details['total_reviews'], app_details['updated_at'],
                app_details['version'], app_details['adSupported'], app_details['ratings'])
    
    cursor.execute('''
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
    ''', app_data)
    
    # Fetch existing reviews for the app
    app_id = app_details['app_id']
    cursor.execute("SELECT review_id, review_date, username, thumbsupcount, score, content FROM Reviews WHERE app_id = %s", (app_id,))
    existing_reviews = {row[0]: row[1:] for row in cursor.fetchall()}

    # Update or insert reviews
    # for review in existing_reviews:
    #     if review[review['review_id']] in new_reviews_list:
    #         # iterate reviews if review id not in new review list  -> pak kon 
    #         # if bood update bokon if ness
    #         # age nabood ham bezaresg
    #         # Check if the review data has changed
    #         if existing_reviews[review['review_id']] != (review['at'], review['userName'], review['thumbsUpCount'], review['score'], review['content']):
    #             # Update the review
    #             update_data = (review['at'], review['userName'], review['thumbsUpCount'], review['score'], review['content'], review['review_id'])
    #             cursor.execute('''
    #                 UPDATE Reviews SET review_date = ?, username = ?, thumbsupcount = ?, score = ?, content = ?
    #                 WHERE review_id = ?
    #             ''', update_data)
    #     else:
    #         # Insert new review
    #         insert_data = (review['review_id'], app_details['app_id'], review['at'], review['userName'], review['thumbsUpCount'], review['score'], review['content'])
    #         cursor.execute('''
    #             INSERT INTO Reviews (review_id, app_id, review_date, username, thumbsupcount, score, content) VALUES (%s, %s, %s, %s, %s, %s, %s)'''
    #             , insert_data)

    # # Commit the transaction and close the connection
    # conn.commit()
    # conn.close()
    
    new_review_ids = {review['review_id'] for review in new_reviews_list}

    # Fetch existing reviews for the app
    cursor.execute("SELECT review_id, review_date, username, thumbsupcount, score, content FROM Reviews WHERE app_id = %s", (app_details['app_id'],))
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
            insert_data = (review['review_id'], app_details['app_id'], review['at'], review['userName'], review['thumbsUpCount'], review['score'], review['content'])
            cursor.execute('''
                INSERT INTO Reviews (review_id, app_id, review_date, username, thumbsupcount, score, content) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', insert_data)

    # Delete reviews that are not in the new reviews list
    reviews_to_delete = existing_reviews.keys() - new_review_ids
    for review_id in reviews_to_delete:
        cursor.execute("DELETE FROM Reviews WHERE review_id = %s", (review_id,))

    # Commit the transaction
    conn.commit()

    # Close the cursor and connection if they won't be used outside this function
    cursor.close()
    conn.close()
