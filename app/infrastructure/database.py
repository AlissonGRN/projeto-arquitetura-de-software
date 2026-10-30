from contextlib import contextmanager
from pathlib import Path
import sqlite3


class Database:
    """Singleton simples responsável por configurar e abrir conexões SQLite."""
    _instance = None

    def __new__(cls, database_path=None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, database_path=None):
        if self._initialized:
            requested = Path(database_path).resolve() if database_path else self.database_path
            if requested != self.database_path:
                raise RuntimeError("O Database já foi configurado com outro caminho.")
            return

        project_root = Path(__file__).resolve().parents[2]
        default_path = project_root / "database" / "db.sqlite"
        self.database_path = Path(database_path).resolve() if database_path else default_path
        self.schema_path = Path(__file__).with_name("schema.sql")
        self._initialized = True

    @classmethod
    def get_instance(cls, database_path=None):
        return cls(database_path)

    def connect(self):
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    @contextmanager
    def connection_scope(self):
        connection = self.connect()
        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def initialize(self):
        schema = self.schema_path.read_text(encoding="utf-8")
        with self.connection_scope() as connection:
            connection.executescript(schema)
