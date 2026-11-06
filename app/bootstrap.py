"""Monta a aplicação e injeta as dependências necessárias."""
import tkinter as tk

from app.application.shopping_facade import ShoppingFacade
from app.application.shopping_service import ShoppingService
from app.infrastructure.database import Database
from app.infrastructure.product_dao import ProductDAO
from app.infrastructure.shopping_list_dao import ShoppingListDAO
from app.presentation.app_controller import AppController


def _build_dependencies(database_path=None):
    database = Database.get_instance(database_path)
    database.initialize()

    shopping_list_dao = ShoppingListDAO(database)
    product_dao = ProductDAO(database)
    service = ShoppingService(shopping_list_dao, product_dao)

    return ShoppingFacade(service), service


def build_facade(database_path=None):
    facade, _ = _build_dependencies(database_path)
    return facade


def run():
    facade, service = _build_dependencies()
    root = tk.Tk()
    AppController(root, facade, service)
    root.mainloop()
