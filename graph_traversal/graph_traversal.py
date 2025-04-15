"""Graph Traversal"""

from graph_traversal import link_generator
from graph_traversal import embedding_traversal
from graph_traversal import random_start_and_end_traversal


class GraphTraversal:
    """Abstract class for graph traversal to easily interchange between different graph traversal
    stratagies"""

    def __init__(self, strategy, openai_client, storage_layer, call_openai=False):
        self.traveral_strategy = None
        if strategy == "embedding_traversal":
            self.traveral_strategy = embedding_traversal.EmbeddingTraversal(
                openai_client, storage_layer, call_openai
            )
        elif strategy == "random_traversal":
            self.traveral_strategy = (
                random_start_and_end_traversal.RandomStartAndEndTraversal(storage_layer)
            )
        else:
            self.traveral_strategy = link_generator.LinkGenerator(
                openai_client, call_openai
            )

    def find_linked_path(self, start, end):
        """Given a start and end topic, find the linked path between the two"""
        return self.traveral_strategy.traverse(start, end)
