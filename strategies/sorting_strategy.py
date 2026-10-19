from abc import ABC, abstractmethod


class SortingStrategy(ABC):

    @abstractmethod
    def sort(self, shopping_lists):
        pass