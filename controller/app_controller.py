from models.shopping_list import ShoppingList
from view.main_menu import MainMenu
from view.shopping_list_view import ShoppingListView
from controller.shopping_list_controller import ShoppingListController


class AppController:
    def __init__(self, root):
        self.root = root

        self.shopping_controller = None

        self.show_main_menu()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_main_menu(self):
        self.clear_window()

        MainMenu(
            self.root,
            on_start=self.show_shopping_list
        )

    def show_shopping_list(self):
        self.clear_window()

        shopping_list = ShoppingList(
            name="Minha Lista de Compras"
        )

        shopping_view = ShoppingListView(
            self.root
        )

        self.shopping_controller = ShoppingListController(
            model=shopping_list,
            view=shopping_view
        )