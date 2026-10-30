from app.domain.money import Money
from app.domain.product import Product


class ProductDAO:
    """DAO que persiste produtos e reconstrói o Money ao consultar."""

    def __init__(self, database):
        self._database = database

    def create(self, list_id: int, product: Product):
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

    def get_by_list_id(self, list_id: int):
        with self._database.connection_scope() as connection:
            rows = connection.execute(
                """SELECT id, list_id, name, quantity, category, price
                   FROM products WHERE list_id = ? ORDER BY id""",
                (list_id,),
            ).fetchall()
        return [self._to_entity(row) for row in rows]

    def delete(self, product_id: int, list_id: int | None = None):
        query = "DELETE FROM products WHERE id = ?"
        parameters = (product_id,)
        if list_id is not None:
            query += " AND list_id = ?"
            parameters += (list_id,)
        with self._database.connection_scope() as connection:
            cursor = connection.execute(query, parameters)
        return cursor.rowcount > 0

    @staticmethod
    def _to_entity(row):
        return Product(
            id=row["id"],
            list_id=row["list_id"],
            name=row["name"],
            quantity=row["quantity"],
            category=row["category"],
            unit_price=Money.from_cents(row["price"]),
        )
