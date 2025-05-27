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
            raise Exception(f"Error while creating database: {e}")

        print(f"Start dumpping to {db_name}")

    def insert_region(self, region: SQLRegion) -> None:
        try:
            self.cursor.execute(
                "INSERT INTO regions (id, name, hexagons) VALUES (?, ?, ?)",
                (region.id, region.name, region.hexagons_blob),
            )
        except sqlite3.Error as e:
            print(e)

    def __del__(self) -> None:
        self.connection.commit()
        self.connection.close()
        print("Connetction closed")


class SQLRegionCellsCount:
    def __init__(self, id: str, name: str, cells_count: int) -> None:
        self.id: str = id
        self.name: str = name
        self.cells_count: int = cells_count


class SQLWriterCellsCount:
    def __init__(self, db_name: str) -> None:
        try:
            self.connection = sqlite3.connect(f"{db_name}.db")
            self.cursor = self.connection.cursor()
            self.cursor.execute(
                "CREATE TABLE IF NOT EXISTS regions_cells_count (id TEXT PRIMARY KEY, name TEXT, cells_count INTEGER)"
            )
            self.connection.commit()
        except sqlite3.Error as e:
            raise Exception(f"Error while creating database: {e}")

        print(f"Start dumpping to {db_name}")

    def insert_region(self, region: SQLRegionCellsCount) -> None:
        try:
            self.cursor.execute(
                "INSERT INTO regions_cells_count (id, name, cells_count) VALUES (?, ?, ?)",
                (region.id, region.name, region.cells_count),
            )
        except sqlite3.Error as e:
            print(e)

    def __del__(self) -> None:
        self.connection.commit()
        self.connection.close()
        print("Connetction closed")
