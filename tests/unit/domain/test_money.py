import unittest
from app.domain.value_objects.money import Money


class MoneyTests(unittest.TestCase):
    def test_parses_brazilian_values(self):
        self.assertEqual(Money.from_brazilian("R$ 1.234,56"), Money(123456))
        self.assertEqual(Money.from_brazilian("10,50"), Money(1050))

    def test_formats_without_float_rounding(self):
        self.assertEqual(Money(123456).format_brl(), "R$ 1.234,56")
        self.assertEqual(Money(5).format_brl(), "R$ 0,05")

    def test_addition_and_multiplication_return_money(self):
        self.assertEqual(Money(250) + Money(175), Money(425))
        self.assertEqual(Money(250) * 3, Money(750))

    def test_rejects_negative_and_non_integer_cents(self):
        with self.assertRaises(ValueError):
            Money(-1)
        with self.assertRaises(TypeError):
            Money(10.5)

    def test_is_immutable(self):
        amount = Money(100)
        with self.assertRaises(AttributeError):
            amount.cents = 200


if __name__ == "__main__":
    unittest.main()
