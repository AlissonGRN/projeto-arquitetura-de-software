from models.product import Product
from models.shopping_list import ShoppingList
from view.shopping_list_view import ShoppingListView


class ShoppingListController:
    def __init__(
        self,
        model: ShoppingList,
        view: ShoppingListView
    ):
        self.model = model
        self.view = view

        self.configure_events()
        self.update_view()

    def configure_events(self):
        self.view.set_add_command(
            self.add_product
        )

        self.view.set_remove_command(
            self.remove_product
        )

    def add_product(self):
        name = self.view.get_product_name().strip()
        quantity_text = self.view.get_quantity().strip()

        if not name:
            self.view.show_error(
                "Informe o nome do produto."
            )
            return

        if not quantity_text:
            self.view.show_error(
                "Informe a quantidade."
            )
            return

        try:
            quantity = int(quantity_text)
        except ValueError:
            self.view.show_error(
                "A quantidade deve ser um número inteiro."
            )
            return

        if quantity <= 0:
            self.view.show_error(
                "A quantidade deve ser maior que zero."
            )
            return

        product = Product(
            name=name,
            quantity=quantity
        )

        self.model.add_product(product)

        self.view.clear_inputs()

        self.update_view()

    def remove_product(self):
        selected_item = self.view.get_selected_item()

        if selected_item is None:
            self.view.show_error(
                "Selecione um produto para remover."
            )
            return

        product_index = int(selected_item)

        if product_index < 0:
            return

        if product_index >= len(self.model.products):
            return

        product = self.model.products[product_index]

        self.model.remove_product(product)

        self.update_view()

    def update_view(self):
        self.view.clear_products()

        for index, product in enumerate(
            self.model.products
        ):
            self.view.add_product_to_table(
                index,
                product.name,
                product.quantity
            )

        total_items = sum(
            product.quantity
            for product in self.model.products
        )

        self.view.update_total(total_items)