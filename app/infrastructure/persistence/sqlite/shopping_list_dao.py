from app.domain.entities.shopping_list import ShoppingList


class ShoppingListDAO:
    """DAO responsável exclusivamente pela tabela shopping_lists."""

    def __init__(self, database):
        self._database = database

    def create(self, shopping_list: ShoppingList) -> ShoppingList:
        with self._database.connection_scope() as connection:
            cursor = connection.execute(
                "INSERT INTO shopping_lists (name) VALUES (?)",
                (shopping_list.name,),
            )
            row = connection.execute(
                "SELECT id, name, created_at FROM shopping_lists WHERE id = ?",
                (cursor.lastrowid,),
            ).fetchone()
        return self._to_entity(row)

    def get_by_id(self, list_id: int) -> ShoppingList | None:
        with self._database.connection_scope() as connection:
            row = connection.execute(
                "SELECT id, name, created_at FROM shopping_lists WHERE id = ?",
                (list_id,),
            ).fetchone()
        return self._to_entity(row) if row else None

    def get_all(self) -> list[ShoppingList]:
        with self._database.connection_scope() as connection:
            rows = connection.execute(
                "SELECT id, name, created_at FROM shopping_lists ORDER BY id"
            ).fetchall()
        return [self._to_entity(row) for row in rows]

    def delete(self, list_id: int) -> bool:
        with self._database.connection_scope() as connection:
            cursor = connection.execute(
                "DELETE FROM shopping_lists WHERE id = ?", (list_id,)
            )
        return cursor.rowcount > 0

    @staticmethod
    def _to_entity(row) -> ShoppingList:
        return ShoppingList(
            id=row["id"],
            name=row["name"],
            created_at=row["created_at"],
        )
