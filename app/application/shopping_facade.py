class ShoppingFacade:
    """Interface simples que encaminha operações para o serviço."""

    def __init__(self, shopping_service):
        self._shopping_service = shopping_service

    def create_list(self, name: str):
        return self._shopping_service.create_list(name)

    def get_list(self, list_id: int):
        return self._shopping_service.get_list(list_id)

    def get_lists(self, sorting_strategy=None):
        return self._shopping_service.get_lists(sorting_strategy)

    def delete_list(self, list_id: int):
        return self._shopping_service.delete_list(list_id)

    def add_product(self, shopping_list, name, quantity, category, unit_price):
        return self._shopping_service.add_product(
            shopping_list, name, quantity, category, unit_price
        )

    def remove_product(self, shopping_list, product):
        return self._shopping_service.remove_product(shopping_list, product)
