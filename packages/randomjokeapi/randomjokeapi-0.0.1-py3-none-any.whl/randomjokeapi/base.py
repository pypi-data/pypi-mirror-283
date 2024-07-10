from abc import ABC, abstractmethod


class Joke(ABC):

    @abstractmethod
    def get_random_joke(self):
        pass