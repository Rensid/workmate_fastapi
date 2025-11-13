from pydantic import BaseModel, ConfigDict
import datetime


class ExchangeProductBase(BaseModel):
    date: datetime.date

    model_config = ConfigDict(from_attributes=True)


class ExchangeProductFilter(ExchangeProductBase):
    oil_id: int
    delivery_basis_id: int
    delivery_type_id: str


class ExchangeProductAll(ExchangeProductFilter):
    delivery_basis_name: str
    exchange_product_id: int
    exchange_product_name: str
    volume: float
    total: float
    count: int
