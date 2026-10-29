import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock

from dao.product_dao import ProductDAO
from facade.shopping_facade import ShoppingFacade


class PersistenceTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database_path = Path(self.temp_dir.name) / "test.sqlite"
        ShoppingFacade.reset_instance()
        self.facade = ShoppingFacade(self.database_path)

    def tearDown(self):
        ShoppingFacade.reset_instance()
        self.temp_dir.cleanup()

    def test_lists_and_products_are_persisted_and_reloaded(self):
        shopping_list = self.facade.create_list("Mercado")
        product = self.facade.add_product(
            shopping_list, "Arroz", 2, "Alimentos", 2599
        )

        self.assertGreater(shopping_list.id, 0)
        self.assertGreater(product.id, 0)
        self.assertEqual(self.facade.get_total_items(shopping_list), 2)
        self.assertEqual(self.facade.get_list_total(shopping_list), 5198)

        ShoppingFacade.reset_instance()
        reloaded = ShoppingFacade(self.database_path)
        loaded_list = reloaded.get_list(shopping_list.id)

        self.assertIsNotNone(loaded_list)
        self.assertEqual(loaded_list.name, "Mercado")
        self.assertEqual(len(loaded_list.products), 1)
        self.assertEqual(loaded_list.products[0].price, 2599)
        self.assertEqual(loaded_list.products[0].quantity, 2)
        self.assertEqual(loaded_list.products[0].category, "Alimentos")

    def test_ids_are_generated_and_lists_are_distinct(self):
        first = self.facade.create_list("A")
        second = self.facade.create_list("B")

        self.assertNotEqual(first.id, second.id)
        self.assertEqual([item.name for item in self.facade.get_lists()], ["A", "B"])

    def test_product_delete_keeps_other_products(self):
        shopping_list = self.facade.create_list("Mercado")
        first = self.facade.add_product(shopping_list, "A", 1, "", 100)
        second = self.facade.add_product(shopping_list, "B", 1, "", 200)

        self.assertTrue(self.facade.remove_product(shopping_list, first))
        self.assertEqual([product.id for product in shopping_list.products], [second.id])
        self.assertFalse(self.facade.remove_product(shopping_list, first))

    def test_list_delete_cascades_products_and_missing_records_fail(self):
        shopping_list = self.facade.create_list("Mercado")
        product = self.facade.add_product(shopping_list, "A", 1, "", 100)

        self.assertTrue(self.facade.delete_list(shopping_list.id))
        self.assertFalse(self.facade.delete_list(shopping_list.id))
        self.assertEqual(ProductDAO(self.database_path).get_by_list_id(shopping_list.id), [])
        self.assertFalse(ProductDAO(self.database_path).delete(product.id))

    def test_failed_product_persistence_does_not_change_model_or_notify(self):
        shopping_list = self.facade.create_list("Mercado")
        observer = Mock()
        shopping_list.add_observer(observer)
        self.facade.product_dao.create = Mock(
            side_effect=sqlite3.IntegrityError("simulated failure")
        )

        with self.assertRaises(sqlite3.IntegrityError):
            self.facade.add_product(shopping_list, "A", 1, "", 100)

        self.assertEqual(shopping_list.products, [])
        observer.update.assert_not_called()


if __name__ == "__main__":
    unittest.main()
