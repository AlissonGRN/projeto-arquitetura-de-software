from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.domain.shopping_list import ShoppingList
    from app.domain.product import Product


class Observer(ABC):
    """Contrato dos objetos que querem receber atualizações."""

    @abstractmethod
    def update(self, event):
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class ShoppingListChanged:
    """Evento publicado quando um produto é adicionado ou removido."""
    shopping_list: "ShoppingList"
    action: str
    product: "Product"
