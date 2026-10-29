from pathlib import Path

from dao.product_dao import ProductDAO
from dao.shopping_list_dao import ShoppingListDAO
from database.connection import DATABASE_PATH, initialize_database
from models.product import Product
from models.shopping_list import ShoppingList



class ShoppingFacade:
    _instance = None

    def __new__(cls, database_path=None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, database_path: str | Path | None = None):
        if getattr(self, "_initialized", False):
            return

        self.database_path = database_path or DATABASE_PATH
        initialize_database(self.database_path)
        self.shopping_list_dao = ShoppingListDAO(self.database_path)
        self.product_dao = ProductDAO(self.database_path)
        self.shopping_lists = {
            shopping_list.id: shopping_list
            for shopping_list in self.shopping_list_dao.get_all()
        }
        for shopping_list in self.shopping_lists.values():
            shopping_list.products = self.product_dao.get_by_list_id(
                shopping_list.id
            )
        self._initialized = True

    @classmethod
    def reset_instance(cls):
        """Reset the Singleton so tests can use isolated databases."""
        cls._instance = None

    # Listas

    def create_list(
        self,
        name: str
    ) -> ShoppingList:
        shopping_list = self.shopping_list_dao.create(name)

        self.shopping_lists[
            shopping_list.id
        ] = shopping_list

        return shopping_list

    def get_list(
        self,
        list_id: int
    ) -> ShoppingList | None:
        return self.shopping_lists.get(list_id)

    def get_lists(
        self
    ) -> list[ShoppingList]:
        return list(
            self.shopping_lists.values()
        )

    def delete_list(
        self,
        list_id: int
    ) -> bool:
        if list_id not in self.shopping_lists:
            return False

        if not self.shopping_list_dao.delete(list_id):
            return False

        del self.shopping_lists[list_id]

        return True

    # Produtos

    def add_product(
        self,
        shopping_list: ShoppingList,
        name: str,
        quantity: int,
        category: str,
        price: int
    ) -> Product:

        product = self.product_dao.create(
            list_id=shopping_list.id,
            name=name,
            quantity=quantity,
            category=category,
            price=price,
        )

        shopping_list.add_product(
            product
        )

        return product

    def remove_product(
        self,
        shopping_list: ShoppingList,
        product: Product
    ) -> bool:
        if not self.product_dao.delete(product.id, shopping_list.id):
            return False

        shopping_list.remove_product(product)
        return True

    # Consultas

    def get_total_items(
        self,
        shopping_list: ShoppingList
    ) -> int:

        return sum(
            product.quantity or 0
            for product in shopping_list.products
        )

    def get_list_total(
        self,
        shopping_list: ShoppingList
    ) -> int:

        return shopping_list.total

