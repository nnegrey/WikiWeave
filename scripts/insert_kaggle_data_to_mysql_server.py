"""
Inserts this kaggle dataset into my local sql server for use
https://www.kaggle.com/datasets/stephanst/wikipedia-simple-openai-embeddings/data

This is mostly just from an LLM, had to simplify quite a bit to parse the json correctly.
"""

import os
import json
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

# Database connection details
DB_CONFIG = {
    "host": "localhost",
    "user": os.environ.get("MYSQL_USER"),
    "password": os.environ.get("MYSQL_PASSWORD"),
    "database": os.environ.get("MYSQL_DBNAME"),
}


def create_table(cursor):
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS page_embeddings (
        title VARCHAR(255),
        content TEXT,
        embedding JSON,
        embedding_model VARCHAR(255)
    )
    """
    )


def insert_data(cursor, title, content, embedding, embedding_model):
    sql = """
    INSERT INTO page_embeddings (title, content, embedding, embedding_model)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(sql, (title, content, json.dumps(embedding), embedding_model))


def process_jsonl_chunk(file_path, chunk_size=1000):
    try:
        cnx = mysql.connector.connect(**DB_CONFIG)
        cursor = cnx.cursor()
        create_table(cursor)
        count = 0
        data_buffer = []

        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    records = json.loads(line)
                    model = records[0].get("model")
                    embedding = records[1]["data"][0]["embedding"]
                    title = None
                    content = None
                    input_str = records[0].get("input")
                    if input_str.startswith("Title:"):
                        parts = input_str.split(" Content:")
                        title = parts[0].replace("Title:", "").strip().replace(" ", "_")
                        content = parts[1].strip() if len(parts) > 1 else None
                    if title and embedding and model:
                        embedding_json = json.dumps(embedding)
                        data_buffer.append((title, content, embedding_json, model))
                        count += 1

                    if count % chunk_size == 0:
                        insert_many_data(cursor, data_buffer)
                        cnx.commit()
                        data_buffer = []
                        print(f"Processed {count} records.")

                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON line: {e} - Line: {line.strip()}")
                except KeyError as e:
                    print(f"Missing key in JSON: {e} - Line: {line.strip()}")

        # Insert any remaining data in the buffer
        if data_buffer:
            insert_many_data(cursor, data_buffer)
            cnx.commit()
            print(
                f"Processed and inserted a total of {count + len(data_buffer)} records."
            )

    except mysql.connector.Error as err:
        print(f"Error connecting or interacting with MySQL: {err}")
    finally:
        if cnx and cnx.is_connected():
            cursor.close()
            cnx.close()


def insert_many_data(cursor, data_list):
    sql = """
    INSERT INTO page_embeddings (title, content, embedding, embedding_model)
    VALUES (%s, %s, %s, %s)
    """
    cursor.executemany(sql, data_list)


if __name__ == "__main__":
    file_path = os.environ.get("KAGGLE_PATH")
    process_jsonl_chunk(file_path)
