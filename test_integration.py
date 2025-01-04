import unittest
from unittest.mock import patch, MagicMock
from integration_prc import create_database_if_needed, create_table_if_needed, execute_sql_file

class TestIntegration(unittest.TestCase):

    @patch('mysql.connector.connect')
    def test_create_database_if_needed(self, mock_connect):
        # Mock database connection and cursor
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        
        # Simulate no database found
        mock_cursor.fetchone.return_value = None
        create_database_if_needed()

        # Assert database creation was attempted
        mock_cursor.execute.assert_any_call("SHOW DATABASES LIKE 'tic_tac_toe'")
        mock_cursor.execute.assert_any_call("CREATE DATABASE tic_tac_toe")

    @patch('mysql.connector.connect')
    def test_create_table_if_needed(self, mock_connect):
        # Mock database connection and cursor
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        
        create_table_if_needed()

        # Assert table creation was attempted
        mock_cursor.execute.assert_called_with('''
        CREATE TABLE IF NOT EXISTS players (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            score INT NOT NULL DEFAULT 0
        );
        ''')

    @patch('mysql.connector.connect')
    def test_execute_sql_file(self, mock_connect):
        # Mock database connection and cursor
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor

        # Mock the SQL file reading
        sql_file_path = 'test.sql'
        sql_content = 'INSERT INTO players (username, score) VALUES ("test_user", 100);'

        with patch('builtins.open', unittest.mock.mock_open(read_data=sql_content)):
            execute_sql_file(sql_file_path)

        # Assert SQL execution was attempted
        mock_cursor.execute.assert_any_call(sql_content, multi=True)

if __name__ == '__main__':
    unittest.main()
