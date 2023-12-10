from google_play_scraper import Sort, reviews
from google_play_scraper import app
from google_play_scraper import search

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

