from app.application.ports.repositories import ProductRepository, ShoppingListRepository
from app.domain.entities.shopping_list import ShoppingList


class ShoppingListService:
    """Orquestra casos de uso relacionados às listas de compras."""

    def __init__(
        self,
        shopping_list_dao: ShoppingListRepository,
        product_dao: ProductRepository,
    ):
        self._shopping_list_dao = shopping_list_dao
        self._product_dao = product_dao

    def create(self, name: str) -> ShoppingList:
        return self._shopping_list_dao.create(ShoppingList(name=name))

    def get_by_id(self, list_id: int) -> ShoppingList | None:
        shopping_list = self._shopping_list_dao.get_by_id(list_id)
        if shopping_list is not None:
            shopping_list.replace_products(self._product_dao.get_by_list_id(list_id))
        return shopping_list

    def get_all(self) -> list[ShoppingList]:
        shopping_lists = self._shopping_list_dao.get_all()
        for shopping_list in shopping_lists:
            shopping_list.replace_products(
                self._product_dao.get_by_list_id(shopping_list.id)
            )
        return shopping_lists

    def delete(self, list_id: int) -> bool:
        return self._shopping_list_dao.delete(list_id)
