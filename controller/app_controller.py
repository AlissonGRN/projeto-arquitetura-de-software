from facade.shopping_facade import ShoppingFacade

from view.main_menu import MainMenu
from view.shopping_list_view import ShoppingListView

from controller.shopping_list_controller import (
    ShoppingListController
)

from strategies.sort_by_id import SortById
from strategies.sort_by_name import SortByName


class AppController:
    def __init__(
        self,
        root,
        facade: ShoppingFacade
    ):
        self.root = root
        self.facade = facade

        self.main_view = None
        self.shopping_controller = None
        self.sorting_strategy = SortById()

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
            on_delete=self.delete_selected_list,
            on_sort_change=self.change_sorting_strategy
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

        self.shopping_controller = (
            ShoppingListController(
                model=shopping_list,
                view=shopping_view,
                facade=self.facade,
                on_back=self.show_main_menu
            )
        )

    # Criar lista

    def create_list(self):
        name = (
            self.main_view
            .get_list_name()
            .strip()
        )

        if not name:
            self.main_view.show_error(
                "Informe um nome para a lista."
            )
            return

        self.facade.create_list(
            name
        )

        self.main_view.clear_name_input()

        self.update_main_menu()

    # Abrir lista

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

        shopping_list = (
            self.facade.get_list(
                list_id
            )
        )

        if shopping_list is None:
            self.main_view.show_error(
                "Lista não encontrada."
            )
            return

        self.show_shopping_list(
            shopping_list
        )

    # Excluir lista

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

        shopping_list = (
            self.facade.get_list(
                list_id
            )
        )

        if shopping_list is None:
            self.main_view.show_error(
                "Lista não encontrada."
            )
            return

        confirmed = (
            self.main_view
            .confirm_delete(
                shopping_list.name
            )
        )

        if not confirmed:
            return

        self.facade.delete_list(
            list_id
        )

        self.update_main_menu()

    # Atualização do menu

    def update_main_menu(self):
        if self.main_view is None:
            return

        self.main_view.clear_lists()

        shopping_lists = self.sorting_strategy.sort(
            self.facade.get_lists()
        )

        for shopping_list in shopping_lists:

            total_items = (
                self.facade
                .get_total_items(
                    shopping_list
                )
            )

            total = (
                self.facade
                .get_list_total(
                    shopping_list
                )
            )

            self.main_view.add_list_to_table(
                list_id=shopping_list.id,
                name=shopping_list.name,
                items=total_items,
                total=total
            )


    # troca o strategy para ordenação
    def change_sorting_strategy(self, choice):
        if choice == "Nome":
            self.sorting_strategy = SortByName()
        else:
            self.sorting_strategy = SortById()

        self.update_main_menu()