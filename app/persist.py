from datetime import datetime
from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursor
from typing import Any


class CalcPersistenceInDB:

    def persist(self, calculation: dict[str, Any]) -> None:
        connection = self._connect()
        cursor = connection.cursor()
        query = """
            INSERT INTO history_tb (
                operation, value_1, value_2, result, date
            ) VALUES (
                %(operation)s,
                %(value_1)s,
                %(value_2)s,
                %(result)s,
                %(date)s
            )
        """
        cursor.execute(query, calculation)
        connection.commit()
        self._close(cursor, connection)

    def get_history_by_date(
        self,
        initial_date: str | datetime | None = None,
        final_date: str | datetime | None = None,
        page: str | int = 1,
        **rest: Any
    ) -> list[dict]:
        connection = self._connect()
        cursor = connection.cursor(dictionary=True)

        query = "SELECT * FROM history_tb"
        where_clause = []
        params = []
        offset = int(page) * 20 - 20

        if initial_date:
            where_clause.append("date >= %s")
            params.append(initial_date)

        if final_date:
            where_clause.append("date <= %s")
            params.append(final_date)

        if where_clause:
            query += " WHERE " + " AND ".join(where_clause)

        query += " ORDER BY date DESC LIMIT %s, 20"
        params.append(offset)

        cursor.execute(query, params)
        history = cursor.fetchall()

        self._close(cursor, connection)
        return history

    def get_calculations_count(self) -> int:
        connection = self._connect()
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM history_tb")

        [[count]] = cursor.fetchall()

        self._close(cursor, connection)
        return count

    @staticmethod
    def _connect() -> MySQLConnection:
        return MySQLConnection(
            host="mysql",
            user="root",
            password="root",
            database="history_db"
        )

    @staticmethod
    def _close(cursor: MySQLCursor, connection: MySQLConnection) -> None:
        cursor.close()
        connection.close()
