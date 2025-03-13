"""Contextual Story Teller"""

from story_teller import simple_story_teller


class StoryTeller:
    """StoryTeller allows for interchangeable stories"""

    def __init__(self, strategy):
        self.story_teller = simple_story_teller.SimpleStoryTeller()

    def generate_story(self, evolutionary_links, call_openai=False):
        """Uses the provided evoultionary_links and the chosen strategy to weave the story."""
        self.story_teller.generate_story(evolutionary_links, call_openai)
