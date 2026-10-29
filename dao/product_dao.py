from pathlib import Path

from database.connection import DATABASE_PATH, connection_scope
from models.product import Product


class ProductDAO:
    """Persists products in SQLite."""

    def __init__(self, database_path: str | Path | None = None):
        self.database_path = database_path or DATABASE_PATH

    def create(
        self,
        list_id: int,
        name: str,
        quantity: int,
        category: str,
        price: int,
    ) -> Product:
        with connection_scope(self.database_path) as connection:
            cursor = connection.execute(
                """
                INSERT INTO products (list_id, name, quantity, category, price)
                VALUES (?, ?, ?, ?, ?)
                """,
                (list_id, name, quantity, category, price),
            )
            product_id = cursor.lastrowid
            row = connection.execute(
                """
                SELECT id, list_id, name, quantity, category, price
                FROM products WHERE id = ?
                """,
                (product_id,),
            ).fetchone()

        return self._to_model(row)

    def get_by_list_id(self, list_id: int) -> list[Product]:
        with connection_scope(self.database_path) as connection:
            rows = connection.execute(
                """
                SELECT id, list_id, name, quantity, category, price
                FROM products WHERE list_id = ? ORDER BY id
                """,
                (list_id,),
            ).fetchall()

        return [self._to_model(row) for row in rows]

    def delete(self, product_id: int, list_id: int | None = None) -> bool:
        query = "DELETE FROM products WHERE id = ?"
        parameters: tuple[int, ...] = (product_id,)
        if list_id is not None:
            query += " AND list_id = ?"
            parameters += (list_id,)

        with connection_scope(self.database_path) as connection:
            cursor = connection.execute(query, parameters)
            return cursor.rowcount > 0

    @staticmethod
    def _to_model(row) -> Product:
        return Product(
            id=row["id"],
            list_id=row["list_id"],
            name=row["name"],
            quantity=row["quantity"] or 0,
            category=row["category"] or "",
            price=row["price"] or 0,
        )
