from models.product import Product
from observer.observer import Observer


class ShoppingList:

    def __init__(
        self,
        id: int = 0,
        name: str = "",
        created_at: str = ""
    ):
        self.id = id
        self.name = name
        self.created_at = created_at

        self.products: list[Product] = []

        self._observers: list[Observer] = []

    # =========================
    # Observer
    # =========================

    def add_observer(
        self,
        observer: Observer
    ) -> None:
        if observer not in self._observers:
            self._observers.append(
                observer
            )

    def remove_observer(
        self,
        observer: Observer
    ) -> None:
        if observer in self._observers:
            self._observers.remove(
                observer
            )

    def notify_observers(self) -> None:
        for observer in self._observers:
            observer.update(self)

    # =========================
    # Dados da lista
    # =========================

    @property
    def total(self) -> int:
        total = 0

        for product in self.products:
            price = product.price or 0
            quantity = product.quantity or 0

            total += price * quantity

        return total

    # =========================
    # Produtos
    # =========================

    def add_product(
        self,
        product: Product
    ) -> None:
        self.products.append(
            product
        )

        self.notify_observers()

    def remove_product(
        self,
        product: Product
    ) -> None:
        self.products.remove(
            product
        )

        self.notify_observers()