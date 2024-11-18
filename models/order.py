from enum import Enum

from pydantic import BaseModel, Field


class Currency(Enum):
    PLN = "PLN"
    EUR = "EUR"
    USD = "USD"


class OrderBody(BaseModel):
    amount: str
    currency: Currency
    firstName: str
    lastName: str
    email: str


class OrderResponse(BaseModel):
    payu_url: str
