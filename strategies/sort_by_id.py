from strategies.sorting_strategy import SortingStrategy


class SortById(SortingStrategy):

    def sort(self, shopping_lists):
        return sorted(
            shopping_lists,
            key=lambda shopping_list: shopping_list.id
        )