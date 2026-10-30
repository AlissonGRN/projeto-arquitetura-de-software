from app.application.strategies.sorting.sorting_strategy import SortingStrategy


class SortById(SortingStrategy):
    def sort(self, shopping_lists: list):
        return sorted(shopping_lists, key=lambda item: item.id or 0)
