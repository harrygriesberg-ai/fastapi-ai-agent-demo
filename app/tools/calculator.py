import operator
from typing import Literal

from pydantic import BaseModel


class CalculatorArgs(BaseModel):
    operation: Literal["add", "subtract", "multiply", "divide"]
    a: float
    b: float


class CalculatorTool:
    name = "calculator"
    description = "Perform basic arithmetic on two numbers."
    args_model = CalculatorArgs

    async def execute(self, arguments: CalculatorArgs) -> dict[str, float]:
        operations = {
            "add": operator.add,
            "subtract": operator.sub,
            "multiply": operator.mul,
            "divide": operator.truediv,
        }
        if arguments.operation == "divide" and arguments.b == 0:
            raise ValueError("division by zero is not allowed")
        value = operations[arguments.operation](arguments.a, arguments.b)
        return {"value": float(value)}
