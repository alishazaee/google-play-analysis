from google_play_scraper import Sort, reviews
from google_play_scraper import app
from google_play_scraper import search

def fetch_reviews(* , app_id:str, count:int):
    result, continuation_token = reviews(
        app_id,
        lang='en',
        country='us', 
        sort=Sort.NEWEST,
        count=count
    )

    return result

def fetch_app_details(app_id):
   
    result = app(
        app_id,
        lang='en',  
        country='us' 
    )

    return {
        "downloads": result.get('installs', 'Unknown'),
        "score": result.get('score', 'Unknown'),
        "total_reviews": result.get('reviews', 'Unknown'),
        "updated_at": result.get('updated', 'Unknown'),
        "version": result.get('version', 'Unknown'),
        "adSupported": result.get('adSupported', 'Unknown'),
        "rating": result.get('contentRating', 'Unknown')  
    }

