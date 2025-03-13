"""Abstract class for StoryTellers"""

from abc import ABC, abstractmethod


class StoryStrategy(ABC):
    """Provides the structure for StoryTellers"""

    @abstractmethod
    def generate_story(self, evolutionary_links, call_openai):
        """Returns the generated the story as text"""
        pass
