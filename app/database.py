from mysql.connector import MySQLConnection

class Database(MySQLConnection):
    __slots__ = ["_cursor"]

    def __init__(self, host, user, password, database):
        super().__init__(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self._cursor = self.cursor()

    def _close(self):
        super().close()

    def close(self):
        self._cursor.close()
        self._close()

    def get_column_names(self, table):
        self._cursor.execute(f"SELECT * FROM {table} LIMIT 1")
        self._cursor.fetchall()

        return self._cursor.column_names

    def select(self, table, columns="*", where=None):
        self._cursor.execute(
            f"SELECT {columns} FROM {table} {'WHERE ' + where if where else ''}"
        )
        result = self._cursor.fetchall()
        self.close()
        
        return result

    def insert(self, table, columns, *values):
        if columns == "*":
            columns = self.get_column_names(table)

        if len(values) > 1:
            values = str(values).removesuffix(")").removeprefix("(")
        elif values:
            values = values[0]

        self._cursor.execute(f"INSERT INTO {table} ({', '.join(columns)}) VALUES {values}")
        self.commit()
        self.close()