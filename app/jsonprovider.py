from typing import Any
from datetime import date
from flask.json.provider import DefaultJSONProvider


class CalcJSONProvider(DefaultJSONProvider):

    @classmethod
    def default(cls, obj: Any) -> Any:
        try:
            if isinstance(obj, date):
                return obj.isoformat()
        except:
            pass

        return super().default(obj)