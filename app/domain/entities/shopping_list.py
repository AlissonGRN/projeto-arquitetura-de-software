from dataclasses import dataclass, field

from app.domain.events.observer import Observer
from app.domain.events.shopping_list_changed import ShoppingListChanged
from app.domain.entities.product import Product
from app.domain.value_objects.money import Money


@dataclass(eq=False, slots=True)
class ShoppingList:
    """Aggregate root: controla produtos e publica alterações aos observadores."""
    name: str
    id: int | None = None
    created_at: str = ""
    products: list[Product] = field(default_factory=list)
    _observers: list[Observer] = field(default_factory=list, init=False, repr=False)

    def __post_init__(self) -> None:
        self.name = self.name.strip()
        if not self.name:
            raise ValueError("A lista precisa ter um nome.")

    def add_observer(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer: Observer) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def _notify(self, action: str, product: Product) -> None:
        event = ShoppingListChanged(self, action, product)
        for observer in tuple(self._observers):
            observer.update(event)

    def add_product(self, product: Product) -> None:
        if product in self.products:
            raise ValueError("Esse produto já está nesta lista.")
        if product.list_id not in (None, self.id):
            raise ValueError("O produto pertence a outra lista.")
        self.products.append(product)
        self._notify("product_added", product)

    def remove_product(self, product: Product) -> None:
        if product not in self.products:
            raise ValueError("O produto não pertence a esta lista.")
        self.products.remove(product)
        self._notify("product_removed", product)

    def replace_products(self, products: list[Product]) -> None:
        """Hidrata o agregado do banco sem publicar evento de alteração."""
        self.products = list(products)

    @property
    def total_items(self) -> int:
        return sum(product.quantity for product in self.products)

    @property
    def total(self) -> Money:
        return sum((product.subtotal for product in self.products), Money.zero())
