"""Story Teller"""

from story_teller import simple_story_teller


class StoryTeller:

    def __init__(self, strategy):
        self.story_teller = simple_story_teller.SimpleStoryTeller()

    def generate_story(self, links):
        self.story_teller.generate_story(links)
