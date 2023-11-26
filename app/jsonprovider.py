from typing import Any
from datetime import date
from flask.json.provider import DefaultJSONProvider
from calculator import Calculation


class CalcJSONProvider(DefaultJSONProvider):

    sort_keys = False

    @classmethod
    def default(cls, obj: Any) -> Any:
        try:
            if isinstance(obj, Calculation):
                return obj.to_dict()

            if isinstance(obj, date):
                return obj.isoformat(timespec="seconds")
        except:
            pass

        return super().default(obj)