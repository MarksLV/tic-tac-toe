import mysql.connector
import logging
import os
from datetime import datetime
from configparser import ConfigParser

# EXECUTION TIME READ
exec_td = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# LOGGING SETUP
cur_dir = os.getcwd()
logger = logging.getLogger()

# CREATION OF LOG FOLDER IF NOT EXISTING
if not os.path.exists(cur_dir + '/Logging'): 
    os.makedirs('Logging')
logging.basicConfig(filename='Logging/integration.log', level=logging.INFO)
logger.info("Started at " + exec_td)

# CONFIG.INI INFO READING
config = ConfigParser()
logger.info("Reading config.ini file...")
config.read('config.ini')

# DATABASE CONNECTION
host = config.get('mysql', 'host')
user = config.get('mysql', 'user')
password = config.get('mysql', 'password')
database = config.get('mysql', 'database')

# CREATING DATABASE IF NEEDED
def create_database_if_needed():
    try:
        # Connect to MySQL server without specifying a database
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        cursor = connection.cursor()

        # CHECK IF DATABASE EXIST
        cursor.execute("SHOW DATABASES LIKE 'tic_tac_toe'")
        result = cursor.fetchone()

        if not result:
            # DATABASE DOESNT EXIST - CREATE
            logger.info("Database 'tic_tac_toe' does not exist. Creating it...")
            cursor.execute("CREATE DATABASE tic_tac_toe")
            logger.info("Database 'tic_tac_toe' created successfully.")
        else:
            logger.info("Database 'tic_tac_toe' already exists.")

        connection.close()

    except mysql.connector.Error as err:
        logger.error(f"Error: Could not connect to the MySQL server. Details: {err}")

# FUNCTION TO CREATE TABLE - IF NEEDED
def create_table_if_needed():
    try:
        # CONNECT TO THE DATABASE
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = connection.cursor()

        # CREATE PLAYERS TABLE - IF NOT EXIST
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            score INT NOT NULL DEFAULT 0
        );
        ''')
        connection.commit()
        logger.info("Table 'players' created successfully or already exists.")

        connection.close()

    except mysql.connector.Error as err:
        logger.error(f"Error: Could not create the table. Details: {err}")

# FUNCTION TO READ THE SQL FILE - EXECUTE QUERIES
def execute_sql_file(file_path):
    try:
        # OPEN SQL FILE - READ CONTENT
        with open(file_path, 'r') as file:
            sql_queries = file.read()

        # CONNECT TO DATABASE
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = connection.cursor()

        # EXECUTE SQL QUERIES
        logger.info("Executing SQL file: " + file_path)
        for result in cursor.execute(sql_queries, multi=True):
            # LOG EACH EXECUTED QUERIEY
            if result.with_rows:
                logger.info(f"Query returned {result.rowcount} rows.")
            else:
                logger.info(f"Query affected {result.rowcount} rows.")
        connection.commit()
        logger.info(f"SQL file '{file_path}' executed successfully.")

        connection.close()

    except mysql.connector.Error as err:
        logger.error(f"Error executing SQL file: {err}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")


# RUN DATABASE - TABLE SETUP PROCESS
if __name__ == "__main__":
    # CREATE DATABASE IF NEEDED
    create_database_if_needed()

    # CREATE TABLE IF NEEDED
    create_table_if_needed()

    # EXECUTE SQL FILE TO INTEGRATE INSIDE DATABASE
    sql_file_path = os.path.join(cur_dir, 'integration', 'tic_tac_toe_players.sql')
    execute_sql_file(sql_file_path)

    logger.info("Integration process complete.")
