"""Embedding Travesral Strategy"""

import ast
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from graph_traversal import traversal_strategy
from embeddings import embedding_generator
from json_data import json_loader


class EmbeddingTraversal(traversal_strategy.TraversalStrategy):
    """Embedding Traversal uses nearest neighbor search to find the evolutionary links
    Implementation:
    1) Embed the user input
    2) Fetch the start / end wikipedia pages whose title's are the best match to the input.
    3) From the start, use the current page's linked pages and compute the distance to the end page
       via the summary embeddings
    4) Cluster the results into 5 evolutionary topics and get a short summary for each
    5) Return the evolutionary links
    """

    def __init__(self, client, storage_layer, call_openai=False):
        self.embed_gen = embedding_generator.EmbeddingGenerator(client)
        self.json_loader = json_loader.JsonLoader()
        self.storage_layer = storage_layer
        self.call_openai = call_openai
        print("\n***** Embedding Traversal Strategy *****")

    def traverse(
        self,
        start,
        end,
        start_description=None,
        end_description=None,
    ):
        # Step 1: Embed user input
        (start_embed, start_desc_embed, end_embed, end_desc_embed) = (
            self.__get_user_input_embeddings(
                start, start_description, end, end_description
            )
        )

        # Step 2: Fetch start nodes linked embeddings
        (start_page, end_page) = self.__get_start_and_end_pages(start_embed, end_embed)

        print(f"Start Point: {start_page["id"]}, {start_page["title"]}")
        print(f"End Point: {end_page["id"]}, {end_page["title"]}")

        # Step 3: Traverse the linked pages
        visited_titles = []
        curr_page = start_page
        while curr_page and len(visited_titles) < 10:
            visited_titles.append(curr_page["title"])

            if end_page["title"] in curr_page["linked_titles"]:
                visited_titles.append(end_page["title"])
                break

            title_embeddings = []
            for link in curr_page["linked_titles"]:
                if link in visited_titles:
                    continue
                embedding = self.storage_layer.get_title_embedding(link)
                if embedding:
                    title_embeddings.append(np.array(embedding))
            title_embeddings = np.array(title_embeddings)
            # Calculate cosine similarities
            similarities = cosine_similarity(
                [np.array(end_page["title_embedding"])],
                title_embeddings,
            )[0]

            # Find the best match
            best_match = np.argmax(similarities)
            curr_page = self.storage_layer.get_path_node_from_title(
                curr_page["linked_titles"][best_match]
            )
        # TODO: Step 4: Cluster embedding results into 5 clusters, summarize the clusters
        # Step 5: Return the evolutionary links
        return visited_titles

    def __get_user_input_embeddings(
        self, start_input, start_description_input, end_input, end_description_input
    ):
        """Embeds the user input"""
        start_embed = None
        end_embed = None
        start_desc_embed = None
        end_desc_embed = None
        if self.call_openai:
            start_embed = self.embed_gen.embed_user_input(start_input)
            end_embed = self.embed_gen.embed_user_input(end_input)
            if start_description_input:
                start_desc_embed = self.embed_gen.embed_user_input(
                    start_description_input
                )
            if end_description_input:
                end_desc_embed = self.embed_gen.embed_user_input(end_description_input)
        else:
            prepped_embeddings = self.__get_canned_start_end_embeddings()
            start_embed = prepped_embeddings["start_input"]
            end_embed = prepped_embeddings["end_input"]
        return (start_embed, start_desc_embed, end_embed, end_desc_embed)

    def __get_start_and_end_pages(self, start_embed, end_embed):
        """For now simply check the whole database to find the best match, because it is a super
        small test dataset.
        """
        # TODO: Setup cluster partitions in the database, so that I can request the cluster
        # embeddings and do the distance on each cluster, then use the cluster_id to find the next
        # cluster until we to a point where we only need to look at some X pages for distance
        # computation.
        (start_page, end_node) = self.storage_layer.find_start_and_end_pages(
            start_embed, end_embed
        )
        return (start_page, end_node)

    def __get_canned_start_end_embeddings(self):
        return self.json_loader.get_json(
            "json_data/sample_output/start_end_response.json"
        )
