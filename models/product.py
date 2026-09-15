
class Product:
    def __init__(
        self,
        id: int = 0,
        list_id: int = 0,
        name: str = "",
        quantity: int = 0,
        category: str = "",
        price: int = 0,
        created_at: str = ""
    ):
        self.id = id
        self.list_id = list_id
        self.name = name
        self.quantity = quantity
        self.category = category
        self.price = price
        self.created_at = created_at
