from pydantic import BaseModel, ConfigDict
import datetime


class ExchangeProductBase(BaseModel):
    date: datetime.date

    model_config = ConfigDict(from_attributes=True)


class ExchangeProductFilter(BaseModel):
    oil_id: str
    delivery_basis_id: str
    delivery_type_id: str


class ExchangeProductAll(ExchangeProductFilter):
    delivery_basis_name: str
    exchange_product_id: str
    exchange_product_name: str
    volume: float
    total: float
    count: int
