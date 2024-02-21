from datetime import date
from typing import Any

from flask.json.provider import DefaultJSONProvider

from calculator import Calculation


class CalculatorJSONProvider(DefaultJSONProvider):

    sort_keys = False

    @classmethod
    def default(cls, obj: Any) -> Any:
        if isinstance(obj, Calculation):
            return obj.to_dict()

        if isinstance(obj, date):
            return obj.isoformat(timespec="seconds")

        return super().default(obj)