from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.domain.events.shopping_list_changed import ShoppingListChanged


class Observer(ABC):
    """Contrato dos objetos interessados em mudanças de uma lista."""

    @abstractmethod
    def update(self, event: "ShoppingListChanged") -> None:
        raise NotImplementedError
