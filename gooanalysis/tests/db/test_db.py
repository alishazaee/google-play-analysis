import unittest
import psycopg2
from gooanalysis.crawler.AppRepository import DB_Connector , AppRepository , ReviewRepository
import unittest
from unittest.mock import MagicMock, patch
import unittest
from unittest.mock import MagicMock, patch

class TestAppRepository(unittest.TestCase):

    @patch('gooanalysis.crawler.AppRepository.DB_Connector')
    def test_create_app_table(self, mock_connector):
        """Test the creation of the Apps and AppAttributes tables."""
        mock_cursor = MagicMock()
        mock_connector.cursor.return_value.__enter__.return_value = mock_cursor

        repo = AppRepository(mock_connector)
        repo.create_app_table()

        # Assert that execute is called with correct SQL commands
        sql_commands = [call[0][0] for call in mock_cursor.execute.call_args_list]
        self.assertIn('CREATE TABLE IF NOT EXISTS Apps', sql_commands[0])
        self.assertIn('CREATE TABLE IF NOT EXISTS AppAttributes', sql_commands[1])

        # Assert that commit is called
        mock_connector.commit.assert_called_once()


    @patch('gooanalysis.crawler.AppRepository.DB_Connector')
    def test_create_reviews_table(self,mock_connector):
        mock_cursor = MagicMock()
        mock_connector.cursor.return_value.__enter__.return_value = mock_cursor
        
        repo = ReviewRepository(mock_connector)
        repo.create_table()

        # Assert that execute is called with correct SQL commands
        sql_commands = [call[0][0] for call in mock_cursor.execute.call_args_list]
        self.assertIn('CREATE TABLE IF NOT EXISTS Reviews', sql_commands[0])

        # Assert that commit is called
        mock_connector.commit.assert_called_once()
