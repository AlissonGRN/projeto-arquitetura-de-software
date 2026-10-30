from app.application.strategies.sorting.sort_by_id import SortById
from app.application.strategies.sorting.sort_by_name import SortByName
from app.application.facades.shopping_facade import ShoppingFacade
from app.presentation.controllers.shopping_list_controller import ShoppingListController
from app.presentation.views.tkinter.main_menu import MainMenu
from app.presentation.views.tkinter.shopping_list_view import ShoppingListView


class AppController:
    """Coordena navegação e traduz ações da tela em chamadas à Facade."""

    def __init__(self, root, facade: ShoppingFacade):
        self.root = root
        self.facade = facade
        self.main_view = None
        self.shopping_controller = None
        self.sorting_strategy = SortById()
        self.show_main_menu()

    def _clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_main_menu(self):
        self._clear_window()
        self.shopping_controller = None
        self.main_view = MainMenu(
            self.root,
            on_create=self.create_list,
            on_open=self.open_selected_list,
            on_delete=self.delete_selected_list,
            on_sort_change=self.change_sorting_strategy,
        )
        self.update_main_menu()

    def show_shopping_list(self, shopping_list):
        self._clear_window()
        view = ShoppingListView(self.root, list_name=shopping_list.name)
        self.shopping_controller = ShoppingListController(
            model=shopping_list,
            view=view,
            facade=self.facade,
            on_back=self.show_main_menu,
        )

    def create_list(self):
        name = self.main_view.get_list_name().strip()
        if not name:
            self.main_view.show_error("Informe um nome para a lista.")
            return
        try:
            self.facade.create_list(name)
        except ValueError as error:
            self.main_view.show_error(str(error))
            return
        self.main_view.clear_name_input()
        self.update_main_menu()

    def open_selected_list(self):
        list_id = self.main_view.get_selected_list_id()
        if list_id is None:
            self.main_view.show_error("Selecione uma lista para abrir.")
            return
        shopping_list = self.facade.get_list(list_id)
        if shopping_list is None:
            self.main_view.show_error("Lista não encontrada.")
            return
        self.show_shopping_list(shopping_list)

    def delete_selected_list(self):
        list_id = self.main_view.get_selected_list_id()
        if list_id is None:
            self.main_view.show_error("Selecione uma lista para excluir.")
            return
        shopping_list = self.facade.get_list(list_id)
        if shopping_list is None:
            self.main_view.show_error("Lista não encontrada.")
            return
        if not self.main_view.confirm_delete(shopping_list.name):
            return
        self.facade.delete_list(list_id)
        self.update_main_menu()

    def update_main_menu(self):
        if self.main_view is None:
            return
        self.main_view.clear_lists()
        for shopping_list in self.facade.get_lists(self.sorting_strategy):
            self.main_view.add_list_to_table(
                list_id=shopping_list.id,
                name=shopping_list.name,
                items=shopping_list.total_items,
                total=shopping_list.total.cents,
            )

    def change_sorting_strategy(self, choice):
        self.sorting_strategy = SortByName() if choice == "Nome" else SortById()
        self.update_main_menu()
