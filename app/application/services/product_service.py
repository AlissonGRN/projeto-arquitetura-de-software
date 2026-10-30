from app.application.ports.repositories import ProductRepository, ShoppingListRepository
from app.domain.entities.product import Product
from app.domain.value_objects.money import Money


class ProductService:
    """Orquestra persistência e atualização do agregado ShoppingList."""

    def __init__(
        self,
        shopping_list_repository: ShoppingListRepository,
        product_repository: ProductRepository,
    ):
        self._shopping_list_repository = shopping_list_repository
        self._product_repository = product_repository

    def add(
        self,
        shopping_list,
        name: str,
        quantity: int,
        category: str,
        unit_price: Money,
    ) -> Product:
        if self._shopping_list_repository.get_by_id(shopping_list.id) is None:
            raise ValueError("A lista não existe mais no banco de dados.")
        candidate = Product(
            name=name,
            quantity=quantity,
            category=category,
            unit_price=unit_price,
            list_id=shopping_list.id,
        )
        # Persistir primeiro: uma falha não altera o agregado nem notifica.
        persisted_product = self._product_repository.create(shopping_list.id, candidate)
        shopping_list.add_product(persisted_product)
        return persisted_product

    def remove(self, shopping_list, product: Product) -> bool:
        if product.id is None:
            return False
        deleted = self._product_repository.delete(product.id, shopping_list.id)
        if not deleted:
            return False
        shopping_list.remove_product(product)
        return True
