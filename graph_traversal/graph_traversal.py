"""Graph Traversal"""

from graph_traversal import link_generator


class GraphTraversal:
    """Abstract class for graph traversal to easily interchange between different graph traversal
    stratagies"""

    def __init__(self, strategy):
        self.traveral_strategy = link_generator.LinkGenerator()

    def find_linked_path(self, start, end, call_openai=False):
        """Given a start and end topic, find the linked path between the two"""
        return self.traveral_strategy.traverse(start, end, call_openai)
