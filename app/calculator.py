class Calculator:
    __slots__ = []
    
    def calculate(self, operation, value1, value2):
        if operation == "sum":
            return self._sum(value1, value2)
        elif operation == "subb":
            return self._subtract(value1, value2)
        elif operation == "multiply":
            return self._multiply(value1, value2)
        elif operation == "divide" and value2:
            return self._divide(value1, value2)

    def _sum(self, value1, value2):
        return value1 + value2
    
    def _subtract(self, value1, value2):
        return value1 - value2

    def _multiply(self, value1, value2):
        return value1 * value2
    
    def _divide(self, value1, value2):
        return value1 / value2
