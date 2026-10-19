from models.product import Product
from models.shopping_list import ShoppingList



class ShoppingFacade:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return

        self.shopping_lists: dict[int, ShoppingList] = {}
        self.next_list_id = 1
        self._initialized = True

    # Listas

    def create_list(
        self,
        name: str
    ) -> ShoppingList:
        shopping_list = ShoppingList(
            id=self.next_list_id,
            name=name
        )

        self.shopping_lists[
            self.next_list_id
        ] = shopping_list

        self.next_list_id += 1

        return shopping_list

    def get_list(
        self,
        list_id: int
    ) -> ShoppingList | None:
        return self.shopping_lists.get(
            list_id
        )

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

        del self.shopping_lists[
            list_id
        ]

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

        product = Product(
            list_id=shopping_list.id,
            name=name,
            quantity=quantity,
            category=category,
            price=price
        )

        shopping_list.add_product(
            product
        )

        return product

    def remove_product(
        self,
        shopping_list: ShoppingList,
        product: Product
    ) -> None:

        shopping_list.remove_product(
            product
        )

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

