from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.domain.entities.product import Product
    from app.domain.entities.shopping_list import ShoppingList


@dataclass(frozen=True, slots=True)
class ShoppingListChanged:
    """Evento enviado pelo agregado após uma alteração confirmada."""
    shopping_list: "ShoppingList"
    action: str
    product: "Product"
