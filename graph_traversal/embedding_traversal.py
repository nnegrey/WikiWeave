"""Embedding Travesral Strategy"""

import ast
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from graph_traversal import traversal_strategy
from embeddings import embedding_generator
from json_data import json_loader


class EmbeddingTraversal(traversal_strategy.TraversalStrategy):
    def __init__(self, client, storage_layer):
        self.embed_gen = embedding_generator.EmbeddingGenerator(client)
        self.json_loader = json_loader.JsonLoader()
        self.storage_layer = storage_layer
        print("\n***** Embedding Traversal Strategy *****")

    def traverse(
        self,
        start,
        end,
        call_openai=False,
        start_description=None,
        end_description=None,
    ):
        # Step 1: Embed user input
        start_embed = None
        end_embed = None
        start_desc_embed = None
        end_desc_embed = None
        if call_openai:
            start_embed = self.embed_gen.embed_user_input(start)
            end_embed = self.embed_gen.embed_user_input(end)
            if start_description:
                start_desc_embed = self.embed_gen.embed_user_input(start_description)
            if end_description:
                end_desc_embed = self.embed_gen.embed_user_input(end_description)
        else:
            prepped_embeddings = self.__get_canned_start_end_embeddings()
            start_embed = prepped_embeddings["start_input"]
            end_embed = prepped_embeddings["end_input"]

        # Step 2: Fetch start nodes linked embeddings
        start_node, end_node = self.storage_layer.find_start_and_end_nodes(
            start_embed, end_embed
        )

        print(f"Start Point: {start_node["id"]}, {start_node["title"]}")
        print(f"End Point: {end_node["id"]}, {end_node["title"]}")

        curr_node = start_node
        path = [curr_node["title"]]
        visited_titles = []
        while end_node["title"] not in path and len(path) < 10:
            visited_titles.append(curr_node["title"])
            links = self.storage_layer.get_links(curr_node["id"])

            if end_node["title"] in links:
                path.append(end_node["title"])
                break

            title_embeddings = []
            titles = []
            for link in links:
                if link in visited_titles:
                    continue
                embedding_str = self.storage_layer.get_embedding_str(link)
                if embedding_str:
                    try:
                        embedding_list = ast.literal_eval(embedding_str)
                        title_embeddings.append(np.array(embedding_list))
                        titles.append(link)
                    except (ValueError, SyntaxError) as e:
                        print(f"Error parsing title embedding string: {e}")
                        return None

            title_embeddings = np.array(title_embeddings)

            # Calculate cosine similarities
            similarities = cosine_similarity(
                [np.array(ast.literal_eval(end_node["title_embedding"]))],
                title_embeddings,
            )[0]

            # Find the best match
            best_match = np.argmax(similarities)
            curr_node = self.storage_layer.get_path_node_from_title(titles[best_match])
            path.append(curr_node["title"])
        # TODO: Cluster embedding results into 5 clusters, summarize the clusters
        return path

    def __get_canned_start_end_embeddings(self):
        return self.json_loader.get_json(
            "json_data/sample_output/start_end_response.json"
        )
