from decimal import Decimal, InvalidOperation

from models.product import Product
from models.shopping_list import ShoppingList
from view.shopping_list_view import ShoppingListView


class ShoppingListController:
    def __init__(
        self,
        model: ShoppingList,
        view: ShoppingListView,
        on_back
    ):
        self.model = model
        self.view = view
        self.on_back = on_back

        self.configure_events()
        self.update_view()

    def configure_events(self):
        self.view.set_add_command(
            self.add_product
        )

        self.view.set_remove_command(
            self.remove_product
        )

        self.view.set_back_command(
            self.on_back
        )

    def add_product(self):
        name = self.view.get_product_name().strip()
        quantity_text = self.view.get_quantity().strip()
        category = self.view.get_category().strip()
        price_text = self.view.get_price().strip()

        # -------------------------
        # Nome
        # -------------------------

        if not name:
            self.view.show_error(
                "Informe o nome do produto."
            )
            return

        # -------------------------
        # Quantidade
        # -------------------------

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

        # -------------------------
        # Categoria
        # -------------------------

        if not category:
            category = "Sem categoria"

        # -------------------------
        # Preço
        # -------------------------

        if not price_text:
            self.view.show_error(
                "Informe o preço do produto."
            )
            return

        try:
            price = self.parse_price_to_cents(
                price_text
            )
        except ValueError:
            self.view.show_error(
                "Informe um preço válido. Exemplo: 10,50"
            )
            return

        if price < 0:
            self.view.show_error(
                "O preço não pode ser negativo."
            )
            return

        # -------------------------
        # Criação do Model
        # -------------------------

        product = Product(
            list_id=self.model.id,
            name=name,
            quantity=quantity,
            category=category,
            price=price
        )

        self.model.add_product(
            product
        )

        self.view.clear_inputs()

        self.update_view()

    def remove_product(self):
        selected_item = self.view.get_selected_item()

        if selected_item is None:
            self.view.show_error(
                "Selecione um produto para excluir."
            )
            return

        product_index = int(
            selected_item
        )

        if product_index < 0:
            return

        if product_index >= len(self.model.products):
            return

        product = self.model.products[
            product_index
        ]

        confirmed = self.view.confirm_delete_product(
            product.name
        )

        if not confirmed:
            return

        self.model.remove_product(
            product
        )

        self.update_view()

    def update_view(self):
        self.view.clear_products()

        for index, product in enumerate(
            self.model.products
        ):
            self.view.add_product_to_table(
                product_index=index,
                name=product.name,
                quantity=product.quantity,
                category=product.category,
                price=product.price
            )

        total_items = sum(
            product.quantity or 0
            for product in self.model.products
        )

        self.view.update_items_total(
            total_items
        )

        self.view.update_price_total(
            self.model.total
        )

    @staticmethod
    def parse_price_to_cents(price_text):
        value = (
            price_text
            .replace("R$", "")
            .replace(" ", "")
            .strip()
        )

        # Formato brasileiro:
        # 1.234,56 -> 1234.56
        if "," in value:
            value = value.replace(
                ".",
                ""
            )

            value = value.replace(
                ",",
                "."
            )

        try:
            decimal_value = Decimal(value)
        except InvalidOperation:
            raise ValueError(
                "Preço inválido"
            )

        if decimal_value < 0:
            raise ValueError(
                "Preço inválido"
            )

        cents = int(
            decimal_value * 100
        )

        return cents