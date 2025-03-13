"""Top-Level Traversal Strategy"""

from abc import ABC, abstractmethod


class TraversalStrategy(ABC):
    """Abstract class for graph traversal to easily interchange between different graph traversal
    stratagies"""

    @abstractmethod
    def traverse(self, start, end):
        """Given a start and end topic, find the linked path between the two"""
        pass
