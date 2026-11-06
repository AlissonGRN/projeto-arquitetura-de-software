import sqlite3

from app.application.commands import (
    AddProductCommand,
    CommandHistory,
    RemoveProductCommand,
)
from app.domain.money import Money
from app.domain.observer import Observer


class ShoppingListController(Observer):
    """Controla a tela de produtos e observa alterações na ShoppingList."""

    def __init__(self, model, view, shopping_service, on_back):
        self.model = model
        self.view = view
        self.shopping_service = shopping_service
        self.on_back = on_back
        self.command_history = CommandHistory()
        self.model.add_observer(self)
        self._configure_events()
        self.update_view()

    def update(self, event):
        if event.shopping_list is self.model:
            self.update_view()

    def _configure_events(self):
        self.view.set_add_command(self.add_product)
        self.view.set_remove_command(self.remove_product)
        self.view.set_undo_command(self.undo)
        self.view.set_redo_command(self.redo)
        self.view.set_back_command(self.go_back)

    def go_back(self):
        self.model.remove_observer(self)
        self.on_back()

    def add_product(self):
        name = self.view.get_product_name().strip()
        quantity_text = self.view.get_quantity().strip()
        category = self.view.get_category().strip() or "Sem categoria"
        price_text = self.view.get_price().strip()

        if not name:
            self.view.show_error("Informe o nome do produto.")
            return
        try:
            quantity = int(quantity_text)
        except ValueError:
            self.view.show_error("A quantidade deve ser um número inteiro.")
            return

        try:
            price = Money.from_brazilian(price_text)
            command = AddProductCommand(
                self.shopping_service, self.model, name, quantity, category, price
            )
            self.command_history.execute(command)
        except (ValueError, TypeError) as error:
            self.view.show_error(str(error))
            return
        except sqlite3.Error:
            self.view.show_error("Não foi possível salvar o produto no banco.")
            return

        self.view.clear_inputs()

    def remove_product(self):
        selected = self.view.get_selected_item()
        if selected is None:
            self.view.show_error("Selecione um produto para excluir.")
            return
        try:
            product = self.model.products[int(selected)]
        except (ValueError, IndexError):
            self.view.show_error("O produto selecionado não está mais disponível.")
            return
        if not self.view.confirm_delete_product(product.name):
            return
        try:
            command = RemoveProductCommand(self.shopping_service, self.model, product)
            self.command_history.execute(command)
        except (ValueError, TypeError) as error:
            self.view.show_error(str(error))
        except sqlite3.Error:
            self.view.show_error("Não foi possível excluir o produto do banco.")

    def undo(self):
        try:
            if not self.command_history.undo():
                self.view.show_error("Não há operação para desfazer.")
                return
        except (ValueError, TypeError) as error:
            self.view.show_error(str(error))
            return
        except sqlite3.Error:
            self.view.show_error("Não foi possível desfazer a operação no banco.")
            return
        self._update_history_buttons()

    def redo(self):
        try:
            if not self.command_history.redo():
                self.view.show_error("Não há operação para refazer.")
                return
        except (ValueError, TypeError) as error:
            self.view.show_error(str(error))
            return
        except sqlite3.Error:
            self.view.show_error("Não foi possível refazer a operação no banco.")
            return
        self._update_history_buttons()

    def update_view(self):
        self.view.clear_products()
        for index, product in enumerate(self.model.products):
            self.view.add_product_to_table(
                product_index=index,
                name=product.name,
                quantity=product.quantity,
                category=product.category,
                price=product.unit_price.cents,
            )
        self.view.update_items_total(self.model.total_items)
        self.view.update_price_total(self.model.total.cents)
        self._update_history_buttons()

    def _update_history_buttons(self):
        self.view.update_history_buttons(
            can_undo=self.command_history.can_undo,
            can_redo=self.command_history.can_redo,
        )
