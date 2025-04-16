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
            get_random_start_and_end_page_sql = """
                SELECT
                    *
                FROM
                    page
                WHERE
                    page_namespace = 0
                    AND page_is_redirect = 0
                    AND page_random >= RAND()
                ORDER BY page_random
                LIMIT 2;
            """
            mycursor.execute(get_random_start_and_end_page_sql)
            start_and_end_page_records = mycursor.fetchall()
            # for row in start_and_end_page_records:
            #     print(row)

            # Step 2: Fetch start/end nodes linked embeddings
            get_embeddings_sql = f"""
                SELECT
                    *
                FROM
                    page_embeddings
                WHERE
                    title = '{self.escape_sql_string(start_and_end_page_records[0][2].decode('utf-8'))}'
                    OR title = '{self.escape_sql_string(start_and_end_page_records[1][2].decode('utf-8'))}'
            """
            mycursor.execute(get_embeddings_sql)
            start_and_end_page_embedding_records = mycursor.fetchall()
            s_idx = 0
            e_idx = 1
            if (
                start_and_end_page_records[0][2]
                != start_and_end_page_embedding_records[0][0]
            ):
                s_idx = 1
                e_idx = 0
            start_page = {
                "id": start_and_end_page_records[0][0],
                "title": start_and_end_page_records[0][2],
                "summary": start_and_end_page_embedding_records[s_idx][1],
                "embedding": [
                    float(val)
                    for val in json.loads(
                        start_and_end_page_embedding_records[s_idx][2]
                    )
                ],
            }
            end_page = {
                "id": start_and_end_page_records[1][0],
                "title": start_and_end_page_records[1][2],
                "summary": start_and_end_page_embedding_records[e_idx][1],
                "embedding": [
                    float(val)
                    for val in json.loads(
                        start_and_end_page_embedding_records[e_idx][2]
                    )
                ],
            }
            # print(start_page["id"], start_page["title"], start_page["summary"])
            # print(end_page["id"], end_page["title"], end_page["summary"])
            print(start_page["id"], start_page["title"])
            print(end_page["id"], end_page["title"])

            # Step 3: Traverse the linked pages
            visited_ids = []
            visited_nodes = []
            curr_page = start_page
            while curr_page and len(visited_ids) < 10:
                visited_ids.append(curr_page["id"])
                visited_nodes.append(curr_page)

                curr_page_links = self.get_page_links(mycursor, curr_page["id"])

                if end_page["id"] in curr_page_links:
                    visited_ids.append(end_page["id"])
                    visited_nodes.append(end_page)
                    break

                page_ids_to_get = []
                for page_id in curr_page_links:
                    if page_id in visited_ids:
                        continue
                    page_ids_to_get.append(page_id)

                pages_and_embeddings = self.get_page_embeddings(
                    mycursor, page_ids_to_get
                )
                title_embeddings = []
                if pages_and_embeddings:
                    for page_and_embedding in pages_and_embeddings:
                        embedding_list_of_floats = [
                            float(val)
                            for val in json.loads(page_and_embedding["embedding"])
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
                curr_page = pages_and_embeddings[best_match]
                # print(
                #     best_match,
                #     curr_page["id"],
                #     curr_page["title"],
                #     curr_page["summary"],
                # )
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

    def get_page_links(self, mycursor, page_id):
        get_page_links_sql = f"""
        SELECT
            pl_target_id
        FROM
            pagelinks
        WHERE
            pl_from = {page_id}
        """
        # print(get_page_links_sql)
        mycursor.execute(get_page_links_sql)
        page_link_records = mycursor.fetchall()
        link_ids = [row[0] for row in page_link_records]
        # print(link_ids)
        return link_ids

    def get_page_embeddings(self, mycursor, page_ids):
        formatted_page_ids = ", ".join(map(str, page_ids))
        get_page_title_sql = f"""
        SELECT
            page_id,
            page_title
        FROM
            page
        WHERE
            page_id IN ({formatted_page_ids})
            AND page_namespace = 0
            AND page_is_redirect = 0
        """
        # print(get_page_title_sql)
        mycursor.execute(get_page_title_sql)
        page_title_records = mycursor.fetchall()
        # for row in page_title_records:
        #     print(row)

        formatted_page_titles = ", ".join(
            map(
                str,
                [
                    f"'{self.escape_sql_string(row[1].decode("utf-8"))}'"
                    for row in page_title_records
                ],
            )
        )
        get_page_embedding_sql = f"""
        SELECT
            title,
            content,
            embedding
        FROM
            page_embeddings
        WHERE
            title IN ({formatted_page_titles})
        """
        # print(get_page_embedding_sql)
        mycursor.execute(get_page_embedding_sql)
        page_embedding_records = mycursor.fetchall()

        pages_and_embeddings = []
        for page_embedding_record in page_embedding_records:
            for page_title_record in page_title_records:
                if page_embedding_record[0] == page_title_record[1].decode("utf-8"):
                    pages_and_embeddings.append(
                        {
                            "id": page_title_record[0],
                            "title": page_title_record[1].decode("utf-8"),
                            "summary": page_embedding_record[1],
                            "embedding": page_embedding_record[2],
                        }
                    )
                    break
        # print(embeddings[0])
        return pages_and_embeddings
