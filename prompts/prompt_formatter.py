from abc import ABC, abstractmethod


class PromptFormatter(ABC):

    @abstractmethod
    def format(self, prompt_args):
        pass
