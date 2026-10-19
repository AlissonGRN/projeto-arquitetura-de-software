from strategies.sorting_strategy import SortingStrategy


class SortByName(SortingStrategy):

    def sort(self, shopping_lists):
        return sorted(
            shopping_lists,
            key=lambda shopping_list: shopping_list.name.lower()
        )