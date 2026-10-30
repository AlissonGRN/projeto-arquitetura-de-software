from app.application.services.product_service import ProductService
from app.application.services.shopping_list_service import ShoppingListService


class ShoppingFacade:
    """Ponto de entrada simplificado; delega o trabalho aos serviços."""

    def __init__(
        self,
        shopping_list_service: ShoppingListService,
        product_service: ProductService,
    ) -> None:
        self._shopping_list_service = shopping_list_service
        self._product_service = product_service

    def create_list(self, name: str):
        return self._shopping_list_service.create(name)

    def get_list(self, list_id: int):
        return self._shopping_list_service.get_by_id(list_id)

    def get_lists(self, sorting_strategy=None):
        return self._shopping_list_service.get_all(sorting_strategy)

    def delete_list(self, list_id: int) -> bool:
        return self._shopping_list_service.delete(list_id)

    def add_product(self, shopping_list, name, quantity, category, unit_price):
        return self._product_service.add(
            shopping_list, name, quantity, category, unit_price
        )

    def remove_product(self, shopping_list, product) -> bool:
        return self._product_service.remove(shopping_list, product)
