import os
from datetime import datetime
from typing import Any

from mysql.connector import MySQLConnection


class CalculationsDB:

    __slots__ = ["_connection", "_cursor"]

    def __init__(self) -> None:
        self._connection = None
        self._cursor = None

    def insert(self, calculation: dict[str, Any]) -> None:
        query = """
            INSERT INTO calculations_tb (
                operation, value_1, value_2, result, date
            ) VALUES (
                %(operation)s,
                %(value_1)s,
                %(value_2)s,
                %(result)s,
                %(date)s
            )
        """
        self._connect()
        self._cursor.execute(query, calculation)
        self._connection.commit()
        self._close()

    def get_calculations(
        self,
        start_date: str | datetime | None = None,
        end_date: str | datetime | None = None,
        page: str | int = 1,
        **rest: Any
    ) -> list[dict]:
        query = "SELECT * FROM calculations_tb"
        where_condition = []
        params = []
        offset = int(page) * 20 - 20

        if start_date:
            where_condition.append("date >= %s")
            params.append(start_date)

        if end_date:
            where_condition.append("date <= %s")
            params.append(end_date)

        if where_condition:
            query += " WHERE " + " AND ".join(where_condition)

        query += " ORDER BY date DESC LIMIT %s, 20"
        params.append(offset)

        self._connect()
        self._cursor.execute(query, params)

        calculations = self._cursor.fetchall()

        self._close()
        return calculations

    def get_calculations_count(self) -> int:
        self._connect()
        self._cursor.execute(
            "SELECT COUNT(*) AS count FROM calculations_tb"
        )
        count = self._cursor.fetchall()[0].get("count")

        self._close()
        return count

    def _connect(self) -> None:
        self._connection = MySQLConnection(
            host=os.getenv("MYSQL_HOST"),
            port=os.getenv("MYSQL_PORT", 3306),
            user="root",
            password=os.getenv("MYSQL_ROOT_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE")
        )
        self._cursor = self._connection.cursor(dictionary=True)

    def _close(self) -> None:
        self._cursor.close()
        self._connection.close()
