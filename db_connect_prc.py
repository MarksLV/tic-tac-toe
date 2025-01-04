import mysql.connector
import logging
import os
from configparser import ConfigParser
from datetime import datetime

# TIME EXECUTION LOGING
exec_td = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# SETUP LOGGING
cur_dir = os.getcwd()
logger = logging.getLogger()

# CREATE LOG FOLDER - IF NOT EXIST
if not os.path.exists(cur_dir + '/Logging'): 
    os.makedirs('Logging')
logging.basicConfig(filename='Logging/db_connect.log', level=logging.INFO)
logger.info("Started at " + exec_td)

# RETRIVE INFO FROM CONFIG.INI
config = ConfigParser()
logger.info("Reading config.ini file...")
config.read('config.ini')

# DATABASE CONNECTION DETAILS
host = config.get('mysql', 'host')
user = config.get('mysql', 'user')
password = config.get('mysql', 'password')
database = config.get('mysql', 'database')

# CHECK DATABASE CONNECTION
def get_db_connection():
    try:
        # CONNECT TO SPECIFIC DATABASE
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        if connection.is_connected():
            logger.info("Database connection successful.")
            return connection
        else:
            logger.error("Failed to connect to the database.")
            return None
    except mysql.connector.Error as err:
        logger.error(f"Error: Could not connect to the database. Details: {err}")
        return None

# IF EXECUTED TEST DATABASE CONNECTION
if __name__ == "__main__":
    conn = get_db_connection()
    if conn is None:
        logger.error("Database connection failed.")
    else:
        logger.info("Database connection successful.")
        conn.close()
