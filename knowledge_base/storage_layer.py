"""Storage Layer for the Wiki Dataset"""

import ast
import pandas as pd
import numpy as np

from sklearn.metrics.pairwise import cosine_similarity

from json_data import json_loader


class StorageLayer:
    """The Storage Layer is the interface for the JSON WikiWeave Dataset

    For now it is simply a JSON file with a test dataset, however I hope to add a real database /
    vector embedding database to store the data in the future. But I think it will always return
    the data in the same JSON format.
    """

    def __init__(self):
        self.json_dataset = json_loader.JsonLoader().get_json(
            "knowledge_base/data/dataset.json"
        )
        self.pages_df = pd.read_csv("knowledge_base/data/pages.csv")
        self.links_df = pd.read_csv("knowledge_base/data/links.csv")
        self.embeddings_df = pd.read_csv("knowledge_base/data/embeddings.csv")

    def __get_embeddigns_best_match_index(self, from_input):
        try:
            input_embedding = np.array(from_input["embedding"])
        except (KeyError, TypeError) as e:
            print(f"Error processing input JSON: {e}")
            return None

        title_embeddings = []
        for embedding_str in self.embeddings_df["title_embedding"]:
            try:
                embedding_list = ast.literal_eval(embedding_str)
                title_embeddings.append(np.array(embedding_list))
            except (ValueError, SyntaxError) as e:
                print(f"Error parsing title embedding string: {e}")
                return None

        title_embeddings = np.array(title_embeddings)

        # Calculate cosine similarities
        similarities = cosine_similarity([input_embedding], title_embeddings)[0]

        # Find the best match
        return np.argmax(similarities)

    def find_start_and_end_pages(self, start_embedding_input, end_embedding_input):
        """Find most relevant entries in DB with embeddings based on title, I don't like having
        logic in my storage layer, but I have to come up with a better solution later.

        Returns a tuple of the start and end nodes
        """
        start_best_match_index = self.__get_embeddigns_best_match_index(
            start_embedding_input
        )
        end_best_match_index = self.__get_embeddigns_best_match_index(
            end_embedding_input
        )

        return (
            self.__get_page_as_json(start_best_match_index),
            self.__get_page_as_json(end_best_match_index),
        )

    # TODO: Probably switch this to id later and store the list of ids instead of titles
    # Optimizations:
    # - return only the summary_embedding
    # - fetch all linked_pages at once
    def get_node(self, title):
        """Get a node from the dataset by title"""
        for page in self.json_dataset["pages"]:
            if page["title"] == title:
                return page
        return None

    def get_path_node_from_title(self, title):
        row = self.pages_df[self.pages_df["title"] == title]
        _id = row.iloc[0]["id"]
        return {
            "id": _id,
            "title": row.iloc[0]["title"],
            "summary": row.iloc[0]["summary"],
            "title_embedding": ast.literal_eval(
                self.embeddings_df.iloc[_id]["title_embedding"]
            ),
            "summary_embedding": ast.literal_eval(
                self.embeddings_df.iloc[_id]["summary_embedding"]
            ),
            "linked_titles": ast.literal_eval(self.links_df.iloc[_id]["linked_titles"]),
        }

    def get_links(self, _id):
        return ast.literal_eval(self.links_df.iloc[_id]["linked_titles"])

    def get_title_embedding(self, title):
        try:
            row = self.pages_df[self.pages_df["title"] == title]

            if not row.empty:
                return ast.literal_eval(
                    self.embeddings_df.iloc[row.iloc[0]["id"]]["title_embedding"]
                )
            else:
                return None

        except KeyError:
            return None  # Handle missing column

    def __get_page_as_json(self, _id):
        return {
            "id": self.pages_df.iloc[_id]["id"],
            "title": self.pages_df.iloc[_id]["title"],
            "summary": self.pages_df.iloc[_id]["summary"],
            "title_embedding": ast.literal_eval(
                self.embeddings_df.iloc[_id]["title_embedding"]
            ),
            "summary_embedding": ast.literal_eval(
                self.embeddings_df.iloc[_id]["summary_embedding"]
            ),
            "linked_titles": ast.literal_eval(self.links_df.iloc[_id]["linked_titles"]),
        }
