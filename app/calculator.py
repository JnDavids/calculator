from typing import Callable
from datetime import datetime


class Calculator:

    __slots__ = ["_operation", "_value1", "_value2", "_result", "_date"]

    def __init__(self, operation: str, value1: int, value2: int) -> None:
        self._operation = operation
        self._value1 = value1
        self._value2 = value2
        self._result = None
        self._date = datetime.utcnow()
        
        self._check_args()
        self.calculate()

    def get_operation(self) -> str:
        return self._operation
    
    def get_value1(self) -> int:
        return self._value1
    
    def get_value2(self) -> int:
        return self._value2
    
    def get_result(self) -> int|float:
        return self._result
    
    def get_date(self) -> datetime:
        return self._date

    def calculate(self) -> None:
        self._result = self._select_operation()()

    def _select_operation(self) -> Callable[[], int|float]:
        operations = {
            "sum": self._sum,
            "subb": self._subtract,
            "multiply": self._multiply,
            "divide": self._divide
        }

        return operations[self._operation]

    def _sum(self) -> int:
        return self._value1 + self._value2
    
    def _subtract(self) -> int:
        return self._value1 - self._value2

    def _multiply(self) -> int:
        return self._value1 * self._value2
    
    def _divide(self) -> float:
        return self._value1 / self._value2

    def _check_args(self) -> None:
        missing_args = []
        invalid_args = []

        if not self._operation:
            missing_args.append("Operator")
        else:
            try:
                self._select_operation()
            except:
                invalid_args.append("Operator")

        if self._value1 is None:
            missing_args.append("Value 1")
        else:
            try:
                float(self._value1)
            except:
                invalid_args.append("Value 1")
        
        if self._value2 is None:
            missing_args.append("Value 2")
        else:
            try:
                float(self._value2)
            except:
                invalid_args.append("Value 2")

        if missing_args or invalid_args:
            raise CalcError(missing_args, invalid_args)


class CalcError(Exception):

    __slots__ = ["_missing_args", "_invalid_args", "_msg"]

    def __init__(
        self,
        missing_args: list[str]|None = None,
        invalid_args: list[str]|None = None
    ) -> None:
        self._missing_args = missing_args
        self._invalid_args = invalid_args
        self._msg = None
        
        self._uptade_msg()

    def __str__(self) -> str:
        return self._msg

    @property
    def msg(self) -> str:
        return self._msg
    
    def _uptade_msg(self) -> None:
        self._msg = ""

        if self._missing_args:
            self._msg += f"Missing {', '.join(self._missing_args)}. "

        if self._invalid_args:
            self._msg += (
                f"{', '.join(self._invalid_args)} "
                f"{'are' if len(self._invalid_args) > 1 else 'is'} invalid."
            )