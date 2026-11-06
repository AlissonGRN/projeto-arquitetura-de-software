from app.application.commands.command import Command
from app.domain.money import Money
from app.domain.product import Product
from app.domain.shopping_list import ShoppingList


class AddProductCommand(Command):
    """Encapsula a adição de um produto para permitir undo e redo."""

    def __init__(
        self,
        shopping_service,
        shopping_list: ShoppingList,
        name: str,
        quantity: int,
        category: str,
        unit_price: Money,
    ):
        self._shopping_service = shopping_service
        self._shopping_list = shopping_list
        self._name = name
        self._quantity = quantity
        self._category = category
        self._unit_price = unit_price
        self._product: Product | None = None

    def execute(self):
        if self._product is None:
            self._product = self._shopping_service.add_product(
                self._shopping_list,
                self._name,
                self._quantity,
                self._category,
                self._unit_price,
            )
        else:
            # No redo, restaura o mesmo registro removido pelo undo,
            # preservando os dados e o ID original.
            self._product = self._shopping_service.restore_product(
                self._shopping_list, self._product
            )
        return self._product

    def undo(self):
        if self._product is None:
            return
        removed = self._shopping_service.remove_product(
            self._shopping_list, self._product
        )
        if not removed:
            raise ValueError("Não foi possível desfazer a adição do produto.")
