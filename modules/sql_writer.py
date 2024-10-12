import sqlite3


class SQLRegion:
    def __init__(self, id: str, name: str, hexagons_blob: bytes) -> None:
        self.id: str = id
        self.name: str = name
        self.hexagons_blob: bytes = hexagons_blob


class SQLWriter:
    def __init__(self, db_name: str) -> None:
        try:
            self.connection = sqlite3.connect(f"{db_name}.db")
            self.cursor = self.connection.cursor()
            self.cursor.execute(
                "CREATE TABLE IF NOT EXISTS regions (id TEXT PRIMARY KEY, name TEXT, hexagons BLOB)"
            )
            self.connection.commit()
        except sqlite3.Error as e:
            print(e)

    def insert_region(self, region: SQLRegion) -> None:
        try:
            self.cursor.execute(
                "INSERT INTO regions (id, name, hexagons) VALUES (?, ?, ?)",
                (region.id, region.name, region.hexagons_blob),
            )
            self.connection.commit()
        except sqlite3.Error as e:
            print(e)
