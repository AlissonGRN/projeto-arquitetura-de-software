from app.application.commands.command import Command
from app.domain.product import Product
from app.domain.shopping_list import ShoppingList


class RemoveProductCommand(Command):
    """Encapsula a remoção de um produto para permitir undo e redo."""

    def __init__(
        self,
        shopping_service,
        shopping_list: ShoppingList,
        product: Product,
    ):
        self._shopping_service = shopping_service
        self._shopping_list = shopping_list
        self._product = product

    def execute(self):
        removed = self._shopping_service.remove_product(
            self._shopping_list, self._product
        )
        if not removed:
            raise ValueError("Não foi possível remover o produto da lista.")
        return self._product

    def undo(self):
        # Reinsere o produto removido com os mesmos dados e o mesmo ID.
        self._product = self._shopping_service.restore_product(
            self._shopping_list, self._product
        )
        return self._product
