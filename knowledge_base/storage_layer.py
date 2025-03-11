"""Storage Layer for the Wiki Dataset"""

# import numpy as np
# import pandas as pd
# import pickle

# from utils.embeddings_utils import (
#     get_embedding,
#     distances_from_embeddings,
#     tsne_components_from_embeddings,
#     chart_from_components,
#     indices_of_nearest_neighbors_from_distances,
# )

from json_data import json_loader


class StorageLayer:
    """The Storage Layer is the interface for the JSON WikiWeave Dataset

    For now it is simply a JSON file with a test dataset, however I hope to add a real database /
    vector embedding database to store the data in the future. But I think it will always return
    the data in the same JSON format.
    """

    def __init__(self):
        self.json_dataset = json_loader.JsonLoader().get_json(
            "knowledge_base/dataset.json"
        )
        self.title_embeddings = []
        self.summary_embeddings = []
        self.id_to_page = {}
        for page in self.json_dataset["pages"]:
            self.title_embeddings.append(page["title_embedding"])
            self.summary_embeddings.append(page["summary_embedding"])
            self.id_to_page[page["id"]] = page

    def find_start_and_end_nodes(self, start_embedding_input, end_embedding_input):
        """Find most relevant entries in DB with embeddings based on title, I don't like having
        logic in my storage layer, but I have to come up with a better solution later.

        Returns a tuple of the start and end nodes
        """
        return self.id_to_page[0], self.id_to_page[1]
        # # Build a FAISS index for efficient similarity search
        # dimension = self.title_embeddings.shape[1]
        # index = faiss.IndexFlatL2(dimension)  # L2 distance (Euclidean)
        # index.add(embeddings)
        # # Finds the best matching Wikipedia title using FAISS.
        # user_embedding = np.expand_dims(
        #     start_embedding_input, axis=0
        # )  # Reshape for faiss
        # distances, indices = index.search(user_embedding, 1)  # Search top 1

        # best_match_index = indices[0][0]
        # best_match_title = wikipedia_titles[best_match_index]
        # return best_match_title

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
