"""Composition root: monta e conecta os componentes da aplicação."""
import tkinter as tk

from app.application.facades.shopping_facade import ShoppingFacade
from app.application.services.product_service import ProductService
from app.application.services.shopping_list_service import ShoppingListService
from app.infrastructure.database.database import Database
from app.infrastructure.persistence.sqlite.product_dao import ProductDAO
from app.infrastructure.persistence.sqlite.shopping_list_dao import ShoppingListDAO
from app.presentation.controllers.app_controller import AppController


def build_facade(database_path=None) -> ShoppingFacade:
    database = Database.get_instance(database_path)
    database.initialize()
    shopping_list_dao = ShoppingListDAO(database)
    product_dao = ProductDAO(database)
    shopping_list_service = ShoppingListService(shopping_list_dao, product_dao)
    product_service = ProductService(shopping_list_dao, product_dao)
    return ShoppingFacade(shopping_list_service, product_service)


def run() -> None:
    facade = build_facade()
    root = tk.Tk()
    AppController(root=root, facade=facade)
    root.mainloop()
