from dataclasses import dataclass
from app.domain.money import Money


@dataclass(slots=True)
class Product:
    """Entidade do domínio que representa um produto da lista."""
    name: str
    quantity: int
    category: str
    unit_price: Money
    id: int | None = None
    list_id: int | None = None

    def __post_init__(self):
        self.name = self.name.strip()
        self.category = self.category.strip() or "Sem categoria"
        if not self.name:
            raise ValueError("O produto precisa ter um nome.")
        if isinstance(self.quantity, bool) or not isinstance(self.quantity, int):
            raise ValueError("A quantidade deve ser um número inteiro.")
        if self.quantity <= 0:
            raise ValueError("A quantidade deve ser maior que zero.")
        if not isinstance(self.unit_price, Money):
            raise TypeError("O preço deve ser um objeto Money.")

    @property
    def subtotal(self):
        return self.unit_price * self.quantity
