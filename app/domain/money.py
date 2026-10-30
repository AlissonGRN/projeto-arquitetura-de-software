from dataclasses import dataclass
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP


@dataclass(frozen=True, slots=True)
class Money:
    """Value Object imutável para representar dinheiro em centavos."""
    cents: int

    def __post_init__(self):
        if isinstance(self.cents, bool) or not isinstance(self.cents, int):
            raise TypeError("O valor em centavos deve ser um número inteiro.")
        if self.cents < 0:
            raise ValueError("O valor monetário não pode ser negativo.")

    @classmethod
    def from_cents(cls, cents: int):
        return cls(cents)

    @classmethod
    def from_brazilian(cls, value: str):
        normalized = value.strip().replace("R$", "").replace(" ", "")
        if not normalized:
            raise ValueError("Informe o preço.")
        if "," in normalized:
            normalized = normalized.replace(".", "").replace(",", ".")
        try:
            amount = Decimal(normalized).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
        except InvalidOperation as error:
            raise ValueError("Preço inválido.") from error
        if not amount.is_finite() or amount < 0:
            raise ValueError("O preço deve ser finito e não negativo.")
        return cls(int(amount * 100))

    def __add__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        return Money(self.cents + other.cents)

    def __mul__(self, quantity: int):
        if isinstance(quantity, bool) or not isinstance(quantity, int):
            raise TypeError("A quantidade deve ser inteira.")
        if quantity < 0:
            raise ValueError("A quantidade não pode ser negativa.")
        return Money(self.cents * quantity)

    def format_brl(self):
        reais, centavos = divmod(self.cents, 100)
        reais_formatados = f"{reais:,}".replace(",", ".")
        return f"R$ {reais_formatados},{centavos:02d}"

    def __str__(self):
        return self.format_brl()
