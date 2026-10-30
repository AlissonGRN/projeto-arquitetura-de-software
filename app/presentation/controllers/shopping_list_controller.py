from app.domain.events.observer import Observer
from app.domain.value_objects.money import Money


class ShoppingListController(Observer):
    """Controller MVC e Observer do agregado ShoppingList."""

    def __init__(self, model, view, facade, on_back):
        self.model = model
        self.view = view
        self.facade = facade
        self.on_back = on_back
        self.model.add_observer(self)
        self._configure_events()
        self.update_view()

    def update(self, event):
        if event.shopping_list is self.model:
            self.update_view()

    def _configure_events(self):
        self.view.set_add_command(self.add_product)
        self.view.set_remove_command(self.remove_product)
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
            unit_price = Money.from_brazilian(price_text)
            self.facade.add_product(
                shopping_list=self.model,
                name=name,
                quantity=quantity,
                category=category,
                unit_price=unit_price,
            )
        except (ValueError, TypeError) as error:
            self.view.show_error(str(error) or "Informe dados válidos.")
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
        self.facade.remove_product(self.model, product)

    def update_view(self):
        self.view.clear_products()
        for index, product in enumerate(self.model.products):
            self.view.add_product_to_table(
                product_index=index,
                name=product.name,
                quantity=product.quantity,
                category=product.category,
                price=product.unit_price.format_brl(),
                subtotal=product.subtotal.format_brl(),
            )
        self.view.update_items_total(self.model.total_items)
        self.view.update_price_total(self.model.total.format_brl())
