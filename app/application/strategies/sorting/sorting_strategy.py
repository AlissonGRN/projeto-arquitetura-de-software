from abc import ABC, abstractmethod


class SortingStrategy(ABC):
    """Contrato comum às estratégias de ordenação."""

    @abstractmethod
    def sort(self, shopping_lists: list):
        raise NotImplementedError
