"""Embedding Travesral Strategy"""

import ast
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from graph_traversal import traversal_strategy
from embeddings import embedding_generator
from json_data import json_loader
import os
from dotenv import load_dotenv

import mysql.connector

load_dotenv()


class RandomStartAndEndTraversal(traversal_strategy.TraversalStrategy):
    """RandomStartAndEnd Traversal uses nearest neighbor search to find the evolutionary links
    Implementation:
    1) Embed the user input
    2) Fetch the start / end wikipedia pages whose title's are the best match to the input.
    3) From the start, use the current page's linked pages and compute the distance to the end page
       via the summary embeddings
    4) Cluster the results into 5 evolutionary topics and get a short summary for each
    5) Return the evolutionary links
    """

    RANDOM_STARRT_AND_END_SQL_PATH = "graph_traversal/random_start_and_end_page.sql"
    GET_LINKED_PAGES_SQL_PATH = "graph_traversal/get_linked_pages.sql"

    def __init__(self, storage_layer):
        self.storage_layer = storage_layer
        print("\n***** RandomStartAndEnd Traversal Strategy *****")

    def traverse(self, start, end):
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user=os.environ.get("MYSQL_USER"),
                password=os.environ.get("MYSQL_PASSWORD"),
                database=os.environ.get("MYSQL_DBNAME"),
            )
            mycursor = mydb.cursor()

            # Step 1: Get two random points
            # Step 2: Fetch start/end nodes linked embeddings
            # TODO: Make sure we always get two results with content and embedding
            start_and_end_page_embedding_records = []
            while len(start_and_end_page_embedding_records) < 2:
                start_and_end_page_embedding_records = self.__execute_sql_from_file(
                    mycursor, self.RANDOM_STARRT_AND_END_SQL_PATH
                )

            start_page = start_and_end_page_embedding_records[0]
            end_page = start_and_end_page_embedding_records[1]
            print(start_page["id"], start_page["title"])
            print(end_page["id"], end_page["title"])

            # Step 3: Traverse the linked pages
            visited_ids = []
            visited_nodes = []
            curr_page = start_page
            while curr_page and len(visited_ids) < 10:
                visited_ids.append(curr_page["id"])
                visited_nodes.append(curr_page)

                curr_pages_links = self.__execute_sql_from_file(
                    mycursor, self.GET_LINKED_PAGES_SQL_PATH, page_id=curr_page["id"]
                )

                unvisted_pages = []
                for linked_page in curr_pages_links:
                    if end_page["id"] == linked_page["id"]:
                        visited_ids.append(end_page["id"])
                        visited_nodes.append(end_page)
                        break
                    if linked_page["id"] in visited_ids:
                        continue
                    unvisted_pages.append(linked_page)

                title_embeddings = []
                if unvisted_pages:
                    for page_node in unvisted_pages:
                        embedding_list_of_floats = [
                            float(val) for val in page_node["embedding"]
                        ]

                        title_embeddings.append(np.array(embedding_list_of_floats))
                title_embeddings = np.array(title_embeddings)
                # Calculate cosine similarities
                similarities = cosine_similarity(
                    [np.array(end_page["embedding"])],
                    title_embeddings,
                )[0]

                # Find the best match
                best_match = np.argmax(similarities)
                curr_page = unvisted_pages[best_match]
            # TODO: Step 4: Cluster embedding results into 5 clusters, summarize the clusters
            # Step 5: Return the evolutionary links
            mycursor.close()
            mydb.close()

            # TODO: Actually try to trace the whole linked path, but for now cut short at 10 nodes
            # and append the end.
            visited_nodes.append(end_page)

            print("\nEvolutionary Links:")
            for node in visited_nodes:
                print(node["id"], node["title"])

            return visited_nodes
        except mysql.connector.Error as err:
            print(f"Error connecting or interacting with MySQL: {err}")
        finally:
            if mydb and mydb.is_connected():
                mycursor.close()
                mydb.close()

    def escape_sql_string(self, value):
        """Escapes single quotes in a string for safe SQL embedding."""
        return value.replace("'", "''")

    def __execute_sql_from_file(self, cursor, file_path, page_id=None):
        try:
            with open(file_path, "r") as file:
                sql_script = file.read().strip()
                if sql_script:
                    if page_id:
                        sql_script = sql_script.format(page_id=page_id)
                    cursor.execute(sql_script)
                    if cursor.with_rows:
                        records = []
                        for row in cursor.fetchall():
                            records.append(self.__get_page_node_from_record(row))
                        return records
                    else:
                        print(f"Executed: {sql_script}")
                        return None
        except FileNotFoundError:
            print(f"Error: SQL file not found at {file_path}")
        except mysql.connector.Error as err:
            print(f"MySQL Error: {err}")

    def __get_page_node_from_record(self, record):
        """Converts a database record into a page node."""
        return {
            "id": record[0],
            "title": record[1],
            "summary": record[2],
            "embedding": [float(val) for val in json.loads(record[3])],
        }
