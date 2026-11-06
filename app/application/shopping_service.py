from app.domain.money import Money
from app.domain.product import Product
from app.domain.shopping_list import ShoppingList


class ShoppingService:
    """Executa os casos de uso e coordena domínio e persistência."""

    def __init__(self, shopping_list_dao, product_dao):
        self.shopping_list_dao = shopping_list_dao
        self.product_dao = product_dao

    def create_list(self, name: str):
        return self.shopping_list_dao.create(ShoppingList(name=name))

    def get_list(self, list_id: int):
        shopping_list = self.shopping_list_dao.get_by_id(list_id)
        if shopping_list is not None:
            products = self.product_dao.get_by_list_id(list_id)
            shopping_list.replace_products(products)
        return shopping_list

    def get_lists(self, sorting_strategy=None):
        shopping_lists = self.shopping_list_dao.get_all()
        for shopping_list in shopping_lists:
            products = self.product_dao.get_by_list_id(shopping_list.id)
            shopping_list.replace_products(products)
        if sorting_strategy is not None:
            return sorting_strategy.sort(shopping_lists)
        return shopping_lists

    def delete_list(self, list_id: int):
        return self.shopping_list_dao.delete(list_id)

    def add_product(
        self,
        shopping_list: ShoppingList,
        name: str,
        quantity: int,
        category: str,
        unit_price: Money,
    ):
        if shopping_list.id is None:
            raise ValueError("Salve a lista antes de adicionar produtos.")
        if self.shopping_list_dao.get_by_id(shopping_list.id) is None:
            raise ValueError("A lista não existe mais no banco.")
        product = Product(
            name=name,
            quantity=quantity,
            category=category,
            unit_price=unit_price,
            list_id=shopping_list.id,
        )
        # O banco é atualizado primeiro. Só depois o Observer é notificado.
        persisted_product = self.product_dao.create(shopping_list.id, product)
        shopping_list.add_product(persisted_product)
        return persisted_product

    def remove_product(self, shopping_list: ShoppingList, product: Product):
        if product.id is None:
            return False
        deleted = self.product_dao.delete(product.id, shopping_list.id)
        if deleted:
            shopping_list.remove_product(product)
        return deleted

    def restore_product(self, shopping_list: ShoppingList, product: Product):
        """Reinsere um produto removido preservando seus dados e ID."""
        if shopping_list.id is None:
            raise ValueError("Salve a lista antes de restaurar produtos.")
        if product.id is None:
            raise ValueError("O produto não possui ID para ser restaurado.")
        if self.shopping_list_dao.get_by_id(shopping_list.id) is None:
            raise ValueError("A lista não existe mais no banco.")
        if any(item.id == product.id for item in shopping_list.products):
            return product
        # O banco é atualizado primeiro. Só depois o Observer é notificado.
        restored_product = self.product_dao.restore(shopping_list.id, product)
        shopping_list.add_product(restored_product)
        return restored_product
