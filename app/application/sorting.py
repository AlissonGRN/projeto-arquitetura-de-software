from abc import ABC, abstractmethod


class SortingStrategy(ABC):
    """Contrato simples para as formas de ordenar listas."""

    @abstractmethod
    def sort(self, shopping_lists: list):
        raise NotImplementedError


class SortById(SortingStrategy):
    def sort(self, shopping_lists: list):
        return sorted(shopping_lists, key=lambda item: item.id or 0)


class SortByName(SortingStrategy):
    def sort(self, shopping_lists: list):
        return sorted(
            shopping_lists,
            key=lambda item: (item.name.casefold(), item.id or 0),
        )
