from pathlib import Path

from database.connection import DATABASE_PATH, connection_scope
from models.shopping_list import ShoppingList


class ShoppingListDAO:
    """Persists shopping lists in SQLite."""

    def __init__(self, database_path: str | Path | None = None):
        self.database_path = database_path or DATABASE_PATH

    def create(self, name: str) -> ShoppingList:
        with connection_scope(self.database_path) as connection:
            cursor = connection.execute(
                "INSERT INTO lists (name) VALUES (?)",
                (name,),
            )
            list_id = cursor.lastrowid
            row = connection.execute(
                "SELECT id, name, created_at FROM lists WHERE id = ?",
                (list_id,),
            ).fetchone()

        return self._to_model(row)

    def get_by_id(self, list_id: int) -> ShoppingList | None:
        with connection_scope(self.database_path) as connection:
            row = connection.execute(
                "SELECT id, name, created_at FROM lists WHERE id = ?",
                (list_id,),
            ).fetchone()

        return self._to_model(row) if row is not None else None

    def get_all(self) -> list[ShoppingList]:
        with connection_scope(self.database_path) as connection:
            rows = connection.execute(
                "SELECT id, name, created_at FROM lists ORDER BY id"
            ).fetchall()

        return [self._to_model(row) for row in rows]

    def delete(self, list_id: int) -> bool:
        with connection_scope(self.database_path) as connection:
            cursor = connection.execute(
                "DELETE FROM lists WHERE id = ?",
                (list_id,),
            )
            return cursor.rowcount > 0

    @staticmethod
    def _to_model(row) -> ShoppingList:
        return ShoppingList(
            id=row["id"],
            name=row["name"] or "",
            created_at=row["created_at"] or "",
        )
