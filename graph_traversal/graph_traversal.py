"""Graph Traversal"""

from graph_traversal import link_generator
from graph_traversal import embedding_traversal


class GraphTraversal:
    """Abstract class for graph traversal to easily interchange between different graph traversal
    stratagies"""

    def __init__(self, strategy, openai_client, storage_layer):
        self.traveral_strategy = None
        if strategy == "embedding_traversal":
            self.traveral_strategy = embedding_traversal.EmbeddingTraversal(
                openai_client, storage_layer
            )
        else:
            self.traveral_strategy = link_generator.LinkGenerator(openai_client)

    def find_linked_path(self, start, end, call_openai=False):
        """Given a start and end topic, find the linked path between the two"""
        return self.traveral_strategy.traverse(start, end, call_openai)
