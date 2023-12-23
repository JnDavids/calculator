from typing import Any, Literal, TypeAlias
from datetime import datetime

Operation: TypeAlias = Literal["sum", "subb", "multiply", "divide"]


class Calculation:

    __slots__ = ["_operation", "_value_1", "_value_2", "_result", "_date"]

    def __init__(
        self,
        operation: Operation,
        value_1: int | float,
        value_2: int | float,
        result: int | float,
        date: datetime
    ) -> None:
        self._operation = operation
        self._value_1 = value_1
        self._value_2 = value_2
        self._result = result
        self._date = date

    operation: Operation = property(lambda self: self._operation)

    value_1: int | float = property(lambda self: self._value_1)

    value_2: int | float = property(lambda self: self._value_2)

    result: int | float = property(lambda self: self._result)

    date: datetime = property(lambda self: self._date)

    def to_dict(self) -> dict[str, Any]:
        return {
            "operation": self._operation,
            "value_1": self._value_1,
            "value_2": self._value_2,
            "result": self._result,
            "date": self._date
        }


class CalcError(Exception):

    __slots__ = ["_missing_args", "_invalid_args", "_msg"]

    def __init__(
        self,
        msg: str | None,
        missing_args: list[str] | None = None,
        invalid_args: list[str] | None = None
    ) -> None:
        self._missing_args = missing_args
        self._invalid_args = invalid_args
        self._msg = msg or self._update_msg()

    def __str__(self) -> str:
        return self._msg

    msg: str = property(lambda self: self._msg)
    
    def _update_msg(self) -> str:
        msg = ""

        if self._missing_args:
            msg += f"Missing {', '.join(self._missing_args)}. "

        if self._invalid_args:
            msg += (
                f"{', '.join(self._invalid_args)} "
                f"{'are' if len(self._invalid_args) > 1 else 'is'} invalid."
            )

        return msg.strip()


class Calculator:

    __slots__ = []

    @classmethod
    def calculate(cls, **kwargs: Any) -> Calculation:
        operation_args = cls._check_args(**kwargs)
        result = cls._make_operation(**operation_args)

        return Calculation(
            **operation_args, result=result, date=datetime.utcnow()
        )

    @staticmethod
    def _make_operation(
        operation: Operation, value_1: int | float, value_2: int | float
    ) -> int | float | None:
        operations = {
            "sum": value_1 + value_2,
            "subb": value_1 - value_2,
            "multiply": value_1 * value_2,
            "divide": value_1 / value_2
        }
        return operations.get(operation)

    @classmethod
    def _check_args(cls, **kwargs: Any) -> dict[str, Any]:
        operation = kwargs.get("operation")
        value_1 = kwargs.get("value_1")
        value_2 = kwargs.get("value_2")

        missing_args = []
        invalid_args = []

        if not operation:
            missing_args.append("Operator")
        elif cls._make_operation(operation, 1, 1) is None:
            invalid_args.append("Operator")

        if value_1 is None or value_1 == "":
            missing_args.append("Value 1")
        else:
            try:
                value_1 = float(value_1)
            except:
                invalid_args.append("Value 1")
        
        if value_2 is None or value_2 == "":
            missing_args.append("Value 2")
        else:
            try:
                value_2 = float(value_2)
            except:
                invalid_args.append("Value 2")

        if missing_args or invalid_args:
            raise CalcError(None, missing_args, invalid_args)
        
        if operation == "divide" and value_2 == 0:
            raise CalcError("Can't divide by zero.")
        
        return {
            "operation": operation, "value_1": value_1, "value_2": value_2
        }