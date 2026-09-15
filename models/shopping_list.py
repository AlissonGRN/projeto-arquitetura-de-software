from models.product import Product


class ShoppingList:

    def __init__(
        self,
        id: int = 0,
        name: str = "",
        created_at: str = ""
    ):
        
        self.id = id
        self.name = name
        self.created_at = created_at
        self.products: list[Product] = []

    @property
    def total(self) -> int:
        total = 0
    
        for product in self.products:
            price = product.price or 0
            quantity = product.quantity or 0
            total += price * quantity
        return total

    def add_product(self, product: Product) -> None:
        self.products.append(product)

    def remove_product(self, product: Product) -> None:
        self.products.remove(product)
