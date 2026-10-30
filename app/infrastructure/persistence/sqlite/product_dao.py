from app.domain.entities.product import Product
from app.domain.value_objects.money import Money


class ProductDAO:
    """DAO que persiste Product e reconstrói seu Value Object Money."""

    def __init__(self, database):
        self._database = database

    def create(self, list_id: int, product: Product) -> Product:
        with self._database.connection_scope() as connection:
            cursor = connection.execute(
                """INSERT INTO products
                   (list_id, name, quantity, category, price)
                   VALUES (?, ?, ?, ?, ?)""",
                (
                    list_id,
                    product.name,
                    product.quantity,
                    product.category,
                    product.unit_price.cents,
                ),
            )
            row = connection.execute(
                """SELECT id, list_id, name, quantity, category, price
                   FROM products WHERE id = ?""",
                (cursor.lastrowid,),
            ).fetchone()
        return self._to_entity(row)

    def get_by_list_id(self, list_id: int) -> list[Product]:
        with self._database.connection_scope() as connection:
            rows = connection.execute(
                """SELECT id, list_id, name, quantity, category, price
                   FROM products WHERE list_id = ? ORDER BY id""",
                (list_id,),
            ).fetchall()
        return [self._to_entity(row) for row in rows]

    def delete(self, product_id: int, list_id: int | None = None) -> bool:
        query = "DELETE FROM products WHERE id = ?"
        parameters: tuple = (product_id,)
        if list_id is not None:
            query += " AND list_id = ?"
            parameters += (list_id,)
        with self._database.connection_scope() as connection:
            cursor = connection.execute(query, parameters)
        return cursor.rowcount > 0

    @staticmethod
    def _to_entity(row) -> Product:
        return Product(
            id=row["id"],
            list_id=row["list_id"],
            name=row["name"],
            quantity=row["quantity"],
            category=row["category"],
            unit_price=Money.from_cents(row["price"]),
        )
