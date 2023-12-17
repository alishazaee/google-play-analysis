import unittest
import psycopg2
from gooanalysis.crawler.AppRepository import AppRepository, ReviewRepository, DB_Connector, fetch_app_details, fetch_reviews

class TestDatabaseOperations(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up a test database connection."""
        cls.connector = DB_Connector()  # Modify as necessary to connect to your test database

        cls.app_repo = AppRepository(cls.connector)
        cls.review_repo = ReviewRepository(cls.connector)

        # Create tables for testing
        cls.app_repo.create_app_table()
        cls.review_repo.create_table()

    def test_insert_app_details(self):
        """Test inserting app details into the database."""
        app_id = 'com.snapchat.android'  # Use a real or dummy app ID
        app_details = fetch_app_details(app_id=app_id)
        self.app_repo.insert_or_update_app_details(app_details)
        with self.connector.cursor() as cursor:
            cursor.execute("SELECT * FROM Apps  where app_id = %s", (app_id,))
            result = cursor.fetchall()
        self.assertIsNotNone(result, "the insertion of app detail is not successful")

    def test_insert_app_attributes(self):
        
        """Test inserting app details into the database."""
        app_id = 'com.snapchat.android'  # Use a real or dummy app ID
        app_details = fetch_app_details(app_id=app_id)
        self.app_repo.insert_or_update_app_details(app_details)
        self.app_repo.insert_or_update_app_attributes(app_details)
        
        
        with self.connector.cursor() as cursor:
            cursor.execute("SELECT * FROM Appattributes WHERE app_id = %s AND installs = %s", (app_id,app_details["installs"])  )
            result = cursor.fetchall()
        self.assertIsNotNone(result , "the insertion of app attr is not successful")
        

    def test_insert_reviews(self):
        """Test inserting reviews into the database."""
        app_id = 'com.snapchat.android'  # Use a real or dummy app ID
        app_details = fetch_app_details(app_id=app_id)
        self.app_repo.insert_or_update_app_details(app_details)

        new_reviews_list = fetch_reviews(app_id=app_id)
        self.review_repo.insert_or_update_reviews(app_id, new_reviews_list)

        with self.connector.cursor() as cursor:
            cursor.execute("SELECT * FROM reviews WHERE app_id =%s" , (app_id,))
            result = cursor.fetchall()
            
        self.assertIsNotNone(result,"there was no reviews ")
        
    @classmethod
    def tearDownClass(cls):
        """Clean up the test database."""
        cls.connector.close()

if __name__ == '__main__':
    unittest.main()
