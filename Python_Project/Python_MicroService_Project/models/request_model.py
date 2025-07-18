from pydantic import BaseModel, conint, confloat


class FibonacciInput(BaseModel):
    n: conint(ge=0)  # integer, n ≥ 0


class FactorialInput(BaseModel):
    n: conint(ge=0)  # integer, n ≥ 0


class PowInput(BaseModel):
    x: confloat()  # float
    y: confloat()  # float
