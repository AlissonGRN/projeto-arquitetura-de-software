from dataclasses import dataclass
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP


@dataclass(frozen=True, slots=True)
class Money:
    """Dinheiro em centavos inteiros; evita erros de ponto flutuante."""
    cents: int

    def __post_init__(self) -> None:
        if isinstance(self.cents, bool) or not isinstance(self.cents, int):
            raise TypeError("Money.cents deve ser um inteiro.")
        if self.cents < 0:
            raise ValueError("O valor monetário não pode ser negativo.")

    @classmethod
    def zero(cls) -> "Money":
        return cls(0)

    @classmethod
    def from_cents(cls, cents: int) -> "Money":
        return cls(cents)

    @classmethod
    def from_decimal(cls, value: Decimal | str | int | float) -> "Money":
        try:
            amount = Decimal(str(value)).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
        except (InvalidOperation, ValueError) as error:
            raise ValueError("Valor monetário inválido.") from error
        if not amount.is_finite() or amount < 0:
            raise ValueError("O valor monetário deve ser finito e não negativo.")
        return cls(int(amount * 100))

    @classmethod
    def from_brazilian(cls, value: str) -> "Money":
        normalized = value.strip().replace("R$", "").replace(" ", "")
        if not normalized:
            raise ValueError("Informe um valor monetário.")
        if "," in normalized:
            normalized = normalized.replace(".", "").replace(",", ".")
        return cls.from_decimal(normalized)

    def __add__(self, other: "Money") -> "Money":
        if not isinstance(other, Money):
            return NotImplemented
        return Money(self.cents + other.cents)

    def __mul__(self, quantity: int) -> "Money":
        if isinstance(quantity, bool) or not isinstance(quantity, int):
            raise TypeError("A multiplicação de Money exige uma quantidade inteira.")
        if quantity < 0:
            raise ValueError("A quantidade não pode ser negativa.")
        return Money(self.cents * quantity)

    def format_brl(self) -> str:
        reais, cents = divmod(self.cents, 100)
        grouped = f"{reais:,}".replace(",", ".")
        return f"R$ {grouped},{cents:02d}"

    def __str__(self) -> str:
        return self.format_brl()
