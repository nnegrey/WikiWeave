"""Embedding Travesral Strategy"""

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
        # curr_node = start_node
        # path = [curr_node, end_node]
        # Step 3: Search via curr_node's linked_pages
        #   - Compute distance of linked_pages to end_node via description_embeddings
        #   - Get best match
        #   - If no more links,
        #       jump from current article to a similar article that has not yet been searched
        #       (use LLM to pick a mid point description between this article and end and then
        #       repeat 2, 3
        #       Go back?
        # Repeat 3 until you reach end
        # Avoid cycles so track path and searched links

        # TODO: Cluster embedding results into 5 clusters, summarize the clusters

        return [start_node["title"], end_node["title"]]

    def __get_canned_start_end_embeddings(self):
        return self.json_loader.get_json(
            "json_data/sample_output/start_end_response.json"
        )
