import os
import time
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.environ.get("MYSQL_HOST", "localhost"),
    "user": os.environ.get("MYSQL_USER"),
    "password": os.environ.get("MYSQL_PASSWORD"),
    "database": os.environ.get("MYSQL_DATABASE", "wikiweave"),
    "port": int(os.environ.get("MYSQL_PORT", "3306")),
}


def get_db_connection(max_retries=10, retry_delay=10):
    """Get a database connection with retry logic."""
    for attempt in range(max_retries):
        try:
            connection = mysql.connector.connect(**DB_CONFIG)
            return connection
        except mysql.connector.Error as err:
            if attempt == max_retries - 1:  # Last attempt
                raise err
            print(f"Database connection attempt {attempt + 1} failed: {err}")
            print(f"Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
