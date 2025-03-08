from abc import ABC, abstractmethod


class StoryStrategy(ABC):

    @abstractmethod
    def generate_story(self, links):
        pass
