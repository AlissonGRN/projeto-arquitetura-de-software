import unittest
from unittest.mock import Mock

from app.domain.entities.product import Product
from app.domain.entities.shopping_list import ShoppingList
from app.domain.value_objects.money import Money


class ObserverTests(unittest.TestCase):
    def setUp(self):
        self.shopping_list = ShoppingList(name="Mercado", id=1)
        self.observer = Mock()

    def test_observer_is_notified_after_product_is_added(self):
        self.shopping_list.add_observer(self.observer)
        product = Product("Arroz", 2, "Alimentos", Money(500), list_id=1)
        self.shopping_list.add_product(product)
        event = self.observer.update.call_args.args[0]
        self.assertEqual(event.action, "product_added")
        self.assertIs(event.shopping_list, self.shopping_list)
        self.assertIs(event.product, product)

    def test_observer_can_be_removed(self):
        self.shopping_list.add_observer(self.observer)
        self.shopping_list.remove_observer(self.observer)
        product = Product("Feijão", 1, "Alimentos", Money(700), list_id=1)
        self.shopping_list.add_product(product)
        self.observer.update.assert_not_called()

    def test_duplicate_subscription_does_not_duplicate_notifications(self):
        self.shopping_list.add_observer(self.observer)
        self.shopping_list.add_observer(self.observer)
        product = Product("Leite", 1, "Alimentos", Money(450), list_id=1)
        self.shopping_list.add_product(product)
        self.assertEqual(self.observer.update.call_count, 1)


if __name__ == "__main__":
    unittest.main()
