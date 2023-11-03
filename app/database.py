from mysql.connector import MySQLConnection


class Database(MySQLConnection):

    __slots__ = ["_cursor"]

    def __init__(
        self, host: str, user: str, password: str, database: str
    ) -> None:
        super().__init__(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self._cursor = self.cursor(dictionary=True)

    def close(self) -> None:
        self._cursor.close()
        super().close()

    def get_column_names(self, table: str) -> tuple[str]:
        self._cursor.execute(f"SELECT * FROM {table} LIMIT 1")
        self._cursor.fetchall()

        return self._cursor.column_names

    def select(
        self, table: str, columns: str = "*", where: str = ""
    ) -> list[dict]:
        self._cursor.execute(
            f"SELECT {columns} FROM {table}"
            f"{where and 'WHERE ' + where}"
        )
        result = self._cursor.fetchall()
        self.close()

        return result

    def insert(self, table: str, columns: str, *values: tuple) -> None:
        if columns == "*":
            columns = ", ".join(self.get_column_names(table))

        if len(values) > 1:
            values = str(values).removesuffix(")").removeprefix("(")
        elif values:
            values = values[0]

        self._cursor.execute(
            f"INSERT INTO {table} ({columns}) VALUES {values}"
        )

        self.commit()
        self.close()