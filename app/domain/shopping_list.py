from dataclasses import dataclass, field

from app.domain.money import Money
from app.domain.observer import Observer, ShoppingListChanged
from app.domain.product import Product


@dataclass(eq=False, slots=True)
class ShoppingList:
    """Entidade e Subject do Observer: mantém os produtos de uma lista."""
    name: str
    id: int | None = None
    created_at: str = ""
    products: list[Product] = field(default_factory=list)
    _observers: list[Observer] = field(default_factory=list, init=False, repr=False)

    def __post_init__(self):
        self.name = self.name.strip()
        if not self.name:
            raise ValueError("A lista precisa ter um nome.")

    def add_observer(self, observer: Observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer: Observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def _notify(self, action: str, product: Product):
        event = ShoppingListChanged(self, action, product)
        for observer in tuple(self._observers):
            observer.update(event)

    def add_product(self, product: Product):
        if product in self.products:
            raise ValueError("Esse produto já está nesta lista.")
        if product.list_id not in (None, self.id):
            raise ValueError("O produto pertence a outra lista.")
        self.products.append(product)
        self._notify("product_added", product)

    def remove_product(self, product: Product):
        if product not in self.products:
            raise ValueError("O produto não pertence a esta lista.")
        self.products.remove(product)
        self._notify("product_removed", product)

    def replace_products(self, products: list[Product]):
        """Carrega os dados do banco sem disparar eventos de alteração."""
        self.products = list(products)

    @property
    def total_items(self):
        return sum(product.quantity for product in self.products)

    @property
    def total(self):
        return sum(
            (product.subtotal for product in self.products),
            Money(0),
        )
