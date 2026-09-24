from decimal import Decimal, InvalidOperation

from facade.shopping_facade import ShoppingFacade

from models.shopping_list import ShoppingList

from observer.observer import Observer

from view.shopping_list_view import ShoppingListView


class ShoppingListController(Observer):

    def __init__(
        self,
        model: ShoppingList,
        view: ShoppingListView,
        facade: ShoppingFacade,
        on_back
    ):
        self.model = model
        self.view = view
        self.facade = facade
        self.on_back = on_back

        # Observer:
        # registra este Controller
        # como observador do Model.
        self.model.add_observer(
            self
        )

        self.configure_events()

        self.update_view()

    # Observer

    def update(self, subject):
        if subject is self.model:
            self.update_view()

    # Eventos

    def configure_events(self):
        self.view.set_add_command(
            self.add_product
        )

        self.view.set_remove_command(
            self.remove_product
        )

        self.view.set_back_command(
            self.go_back
        )

    def go_back(self):
        self.model.remove_observer(
            self
        )

        self.on_back()

    # Adicionar produto

    def add_product(self):
        name = (
            self.view
            .get_product_name()
            .strip()
        )

        quantity_text = (
            self.view
            .get_quantity()
            .strip()
        )

        category = (
            self.view
            .get_category()
            .strip()
        )

        price_text = (
            self.view
            .get_price()
            .strip()
        )

        # Nome

        if not name:
            self.view.show_error(
                "Informe o nome do produto."
            )
            return

        # Quantidade

        if not quantity_text:
            self.view.show_error(
                "Informe a quantidade."
            )
            return

        try:
            quantity = int(
                quantity_text
            )

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

        # Categoria

        if not category:
            category = "Sem categoria"

        # Preço

        if not price_text:
            self.view.show_error(
                "Informe o preço do produto."
            )
            return

        try:
            price = (
                self.parse_price_to_cents(
                    price_text
                )
            )

        except ValueError:
            self.view.show_error(
                "Informe um preço válido. "
                "Exemplo: 10,50"
            )
            return

        # Facade

        self.facade.add_product(
            shopping_list=self.model,
            name=name,
            quantity=quantity,
            category=category,
            price=price
        )

        self.view.clear_inputs()

    # Remover produto

    def remove_product(self):
        selected_item = (
            self.view
            .get_selected_item()
        )

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

        if product_index >= len(
            self.model.products
        ):
            return

        product = self.model.products[
            product_index
        ]

        confirmed = (
            self.view
            .confirm_delete_product(
                product.name
            )
        )

        if not confirmed:
            return

        self.facade.remove_product(
            shopping_list=self.model,
            product=product
        )

    # Atualização da View

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

        total_items = (
            self.facade
            .get_total_items(
                self.model
            )
        )

        total_price = (
            self.facade
            .get_list_total(
                self.model
            )
        )

        self.view.update_items_total(
            total_items
        )

        self.view.update_price_total(
            total_price
        )

    # Conversão de preço

    @staticmethod
    def parse_price_to_cents(
        price_text
    ):
        value = (
            price_text
            .replace("R$", "")
            .replace(" ", "")
            .strip()
        )

        # Formato brasileiro:
        #
        # 10,50
        # 1.234,56
        #
        # vira:
        #
        # 10.50
        # 1234.56

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
            decimal_value = Decimal(
                value
            )

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