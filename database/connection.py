import sqlite3
from contextlib import contextmanager
from pathlib import Path


DATABASE_DIRECTORY = Path(__file__).resolve().parent
DATABASE_PATH = DATABASE_DIRECTORY / "db.sqlite"
SCHEMA_PATH = DATABASE_DIRECTORY / "schema.sql"


def get_connection(database_path=None):
    path = Path(database_path) if database_path is not None else DATABASE_PATH
    connection = sqlite3.connect(path)
    connection.execute("PRAGMA foreign_keys = ON")
    connection.row_factory = sqlite3.Row

    return connection


@contextmanager
def connection_scope(database_path=None):
    connection = get_connection(database_path)
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def initialize_database(database_path=None):
    connection = get_connection(database_path)

    try:
        schema = SCHEMA_PATH.read_text(encoding="utf-8")
        connection.executescript(schema)
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
