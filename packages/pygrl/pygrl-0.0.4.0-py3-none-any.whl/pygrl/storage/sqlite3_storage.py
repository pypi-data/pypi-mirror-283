import json
import os
import re
import sqlite3
from typing import Any
from .storage import Storage


class SQLite3_Storage(Storage):
    """
    SQLite3_Storage is a subclass of the Storage abstract base class.
    This class provides a concrete implementation of the Storage interface using SQLite3 as the storage system.
    It stores key-value pairs in a SQLite3 database.

    Attributes:
    db_path (str): The path to the SQLite3 database.
    table_name (str): The name of the table in the SQLite3 database.
    """

    def __init__(self, db_path: str, table_name: str = "storage", overwrite: bool = False):
        """
        Initializes a new instance of the SQLite3_Storage class.

        Args:
        db_path (str): The path to the SQLite3 database.
        table_name (str, optional): The name of the table in the SQLite3 database. Defaults to "storage".
        overwrite (bool, optional): If True, overwrites the existing database at db_path. Defaults to False.
        """
        self.db_path = db_path
        self.table_name = table_name
        self.init(db_path, table_name, overwrite)

    @classmethod
    def init(cls, db_path: str, table_name: str, overwrite: bool = False):
        """
        Initializes the SQLite3 database.

        Args:
        db_path (str): The path to the SQLite3 database.
        table_name (str): The name of the table in the SQLite3 database.
        overwrite (bool, optional): If True, overwrites the existing database at db_path. Defaults to False.
        """
        _ = [
            SQLite3_Storage.validate_db_path(db_path),
            SQLite3_Storage.validate_table_name(table_name)
        ]  # Exception will be raised if validation fails

        if overwrite:
            if os.path.exists(db_path):
                os.remove(db_path)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (key TEXT PRIMARY KEY, value TEXT)")
        conn.commit()

    @classmethod
    def validate_db_path(cls, db_path: str):
        if not isinstance(db_path, str):
            raise ValueError(f"Invalid database path: {db_path}")

        if not db_path:
            raise ValueError("Database path cannot be empty")

        if not os.path.basename(db_path):
            raise ValueError(f"Invalid database path: {db_path}")

    @classmethod
    def validate_table_name(cls, table_name: str):
        if not isinstance(table_name, str):
            raise ValueError(f"Invalid table name: {table_name}")

        if not table_name:
            raise ValueError("Table name cannot be empty")

        if re.search(r"^\w+$", table_name) is None:
            raise ValueError(f"Invalid table name: {table_name}")

    def get(self, key: str):
        """
        Retrieves the value associated with the given key from the SQLite3 database.

        Args:
        key (str): The key to retrieve the value for.

        Returns:
        Any: The value associated with the given key, or None if the key does not exist.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(f"SELECT value FROM {self.table_name} WHERE key=?", (key,))
        result = cursor.fetchone()
        if result:
            return json.loads(result[0])
        return None

    def set(self, key: str, value: Any):
        """
        Sets the value for the given key in the SQLite3 database.

        Args:
        key (str): The key to set the value for.
        value (Any): The value to set.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(f"INSERT OR REPLACE INTO {self.table_name} (key, value) VALUES (?, ?)",
                       (key, json.dumps(value)))
        conn.commit()

    def drop(self, key: str):
        """
        Deletes the key-value pair associated with the given key from the SQLite3 database.

        Args:
        key (str): The key to delete the value for.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {self.table_name} WHERE key=?", (key,))
        conn.commit()

    def clear(self):
        """
        Deletes all key-value pairs from the SQLite3 database.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {self.table_name}")
        conn.commit()

    def keys(self) -> list[str]:
        """
        Returns a list of all keys in the SQLite3 database.

        Returns:
        list[str]: A list of all keys in the SQLite3 database.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(f"SELECT key FROM {self.table_name}")
        return [row[0] for row in cursor.fetchall()]
