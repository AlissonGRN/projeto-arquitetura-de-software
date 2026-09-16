from models.shopping_list import ShoppingList

from view.main_menu import MainMenu
from view.shopping_list_view import ShoppingListView

from controller.shopping_list_controller import (
    ShoppingListController
)


class AppController:
    def __init__(self, root):
        self.root = root

        self.shopping_lists = {}
        self.next_list_id = 1

        self.main_view = None
        self.shopping_controller = None

        self.show_main_menu()

    # =========================
    # Navegação
    # =========================

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_main_menu(self):
        self.clear_window()

        self.shopping_controller = None

        self.main_view = MainMenu(
            self.root,
            on_create=self.create_list,
            on_open=self.open_selected_list,
            on_delete=self.delete_selected_list
        )

        self.update_main_menu()

    def show_shopping_list(
        self,
        shopping_list
    ):
        self.clear_window()

        shopping_view = ShoppingListView(
            self.root,
            list_name=shopping_list.name
        )

        self.shopping_controller = ShoppingListController(
            model=shopping_list,
            view=shopping_view,
            on_back=self.show_main_menu
        )

    # =========================
    # Listas
    # =========================

    def create_list(self):
        name = self.main_view.get_list_name().strip()

        if not name:
            self.main_view.show_error(
                "Informe um nome para a lista."
            )
            return

        shopping_list = ShoppingList(
            id=self.next_list_id,
            name=name
        )

        self.shopping_lists[
            self.next_list_id
        ] = shopping_list

        self.next_list_id += 1

        self.main_view.clear_name_input()

        self.update_main_menu()

    def open_selected_list(self):
        list_id = (
            self.main_view
            .get_selected_list_id()
        )

        if list_id is None:
            self.main_view.show_error(
                "Selecione uma lista para abrir."
            )
            return

        shopping_list = self.shopping_lists.get(
            list_id
        )

        if shopping_list is None:
            self.main_view.show_error(
                "Lista não encontrada."
            )
            return

        self.show_shopping_list(
            shopping_list
        )

    def delete_selected_list(self):
        list_id = (
            self.main_view
            .get_selected_list_id()
        )

        if list_id is None:
            self.main_view.show_error(
                "Selecione uma lista para excluir."
            )
            return

        shopping_list = self.shopping_lists.get(
            list_id
        )

        if shopping_list is None:
            self.main_view.show_error(
                "Lista não encontrada."
            )
            return

        confirmed = self.main_view.confirm_delete(
            shopping_list.name
        )

        if not confirmed:
            return

        del self.shopping_lists[
            list_id
        ]

        self.update_main_menu()

    def update_main_menu(self):
        if self.main_view is None:
            return

        self.main_view.clear_lists()

        for list_id, shopping_list in (
            self.shopping_lists.items()
        ):
            total_items = sum(
                product.quantity or 0
                for product in shopping_list.products
            )

            self.main_view.add_list_to_table(
                list_id=list_id,
                name=shopping_list.name,
                items=total_items,
                total=shopping_list.total
            )