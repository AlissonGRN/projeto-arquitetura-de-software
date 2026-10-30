from app.domain.shopping_list import ShoppingList


class ShoppingListDAO:
    """DAO que concentra as consultas e gravações da tabela lists."""

    def __init__(self, database):
        self._database = database

    def create(self, shopping_list: ShoppingList):
        with self._database.connection_scope() as connection:
            cursor = connection.execute(
                "INSERT INTO lists (name) VALUES (?)",
                (shopping_list.name,),
            )
            row = connection.execute(
                "SELECT id, name, created_at FROM lists WHERE id = ?",
                (cursor.lastrowid,),
            ).fetchone()
        return self._to_entity(row)

    def get_by_id(self, list_id: int):
        with self._database.connection_scope() as connection:
            row = connection.execute(
                "SELECT id, name, created_at FROM lists WHERE id = ?",
                (list_id,),
            ).fetchone()
        return self._to_entity(row) if row else None

    def get_all(self):
        with self._database.connection_scope() as connection:
            rows = connection.execute(
                "SELECT id, name, created_at FROM lists ORDER BY id"
            ).fetchall()
        return [self._to_entity(row) for row in rows]

    def delete(self, list_id: int):
        with self._database.connection_scope() as connection:
            cursor = connection.execute(
                "DELETE FROM lists WHERE id = ?", (list_id,)
            )
        return cursor.rowcount > 0

    @staticmethod
    def _to_entity(row):
        return ShoppingList(
            id=row["id"],
            name=row["name"],
            created_at=row["created_at"],
        )
