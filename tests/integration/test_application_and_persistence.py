import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock

from app.bootstrap import build_facade
from app.domain.value_objects.money import Money
from app.infrastructure.database.database import Database
from app.infrastructure.persistence.sqlite.product_dao import ProductDAO
from app.application.strategies.sorting.sort_by_id import SortById
from app.application.strategies.sorting.sort_by_name import SortByName


class ApplicationAndPersistenceTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database_path = Path(self.temp_dir.name) / "test.sqlite3"
        Database.reset_instance()
        self.facade = build_facade(self.database_path)

    def tearDown(self):
        Database.reset_instance()
        self.temp_dir.cleanup()

    def test_lists_and_products_are_persisted_and_reloaded_as_domain_objects(self):
        shopping_list = self.facade.create_list("Mercado")
        product = self.facade.add_product(
            shopping_list, "Arroz", 2, "Alimentos", Money(2599)
        )
        self.assertGreater(shopping_list.id, 0)
        self.assertEqual(product.unit_price, Money(2599))
        self.assertEqual(shopping_list.total, Money(5198))

        Database.reset_instance()
        reloaded_facade = build_facade(self.database_path)
        loaded = reloaded_facade.get_list(shopping_list.id)
        self.assertEqual(len(loaded.products), 1)
        self.assertIsInstance(loaded.products[0].unit_price, Money)
        self.assertEqual(loaded.products[0].unit_price, Money(2599))
        self.assertEqual(loaded.total.format_brl(), "R$ 51,98")

    def test_product_delete_and_list_cascade(self):
        shopping_list = self.facade.create_list("Mercado")
        product = self.facade.add_product(shopping_list, "Arroz", 1, "", Money(100))
        self.assertTrue(self.facade.remove_product(shopping_list, product))
        self.assertFalse(self.facade.remove_product(shopping_list, product))
        self.facade.add_product(shopping_list, "Feijão", 1, "", Money(200))
        self.assertTrue(self.facade.delete_list(shopping_list.id))
        self.assertEqual(
            ProductDAO(Database.get_instance(self.database_path)).get_by_list_id(shopping_list.id),
            [],
        )
        self.assertFalse(self.facade.delete_list(shopping_list.id))

    def test_failed_persistence_does_not_mutate_aggregate_or_notify(self):
        shopping_list = self.facade.create_list("Mercado")
        observer = Mock()
        shopping_list.add_observer(observer)
        self.facade._product_service._product_dao.create = Mock(
            side_effect=sqlite3.IntegrityError("simulated failure")
        )
        with self.assertRaises(sqlite3.IntegrityError):
            self.facade.add_product(shopping_list, "Arroz", 1, "", Money(100))
        self.assertEqual(shopping_list.products, [])
        observer.update.assert_not_called()

    def test_strategy_changes_order_without_changing_source(self):
        self.facade.create_list("Zebra")
        self.facade.create_list("Arroz")
        self.facade.create_list("Mercado")
        self.assertEqual(
            [item.name for item in self.facade.get_lists(SortById())],
            ["Zebra", "Arroz", "Mercado"],
        )
        self.assertEqual(
            [item.name for item in self.facade.get_lists(SortByName())],
            ["Arroz", "Mercado", "Zebra"],
        )
        self.assertEqual(
            [item.name for item in self.facade.get_lists()],
            ["Zebra", "Arroz", "Mercado"],
        )

    def test_database_manager_is_singleton_and_rejects_second_configuration(self):
        first = Database.get_instance(self.database_path)
        second = Database.get_instance(self.database_path)
        self.assertIs(first, second)
        with self.assertRaises(RuntimeError):
            Database.get_instance(Path(self.temp_dir.name) / "other.sqlite3")


if __name__ == "__main__":
    unittest.main()
