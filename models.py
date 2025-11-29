from datetime import date, datetime
from typing import Annotated, Optional

from sqlalchemy import Date, DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from base import Base

date_field = Annotated[date, mapped_column(DateTime, default=datetime.utcnow)]


class ExchangeProduct(Base):
    __tablename__ = "exchange_products"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    exchange_product_id: Mapped[str] = mapped_column(
        String, nullable=False, unique=True
    )
    exchange_product_name: Mapped[str] = mapped_column(String, nullable=False)

    oil_id: Mapped[str] = mapped_column(String, nullable=False)
    delivery_basis_id: Mapped[str] = mapped_column(String)
    delivery_basis_name: Mapped[str] = mapped_column(String, nullable=False)
    delivery_type_id: Mapped[str] = mapped_column(String)

    volume: Mapped[Optional[float]] = mapped_column(Float)
    total: Mapped[Optional[float]] = mapped_column(Float)
    count: Mapped[Optional[int]] = mapped_column(Integer)

    date: Mapped[date] = mapped_column(Date, nullable=False)

    created_on: Mapped[date_field]
    updated_on: Mapped[Annotated[date_field, mapped_column(onupdate=datetime.utcnow)]]

    def __repr__(self) -> str:
        return (
            f"<ExchangeProduct(id={self.id}, name={self.exchange_product_name!r}, "
            f"date={self.date}, exchange_product_id={self.exchange_product_id!r})>"
        )

    def to_dict(self):
        product_dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        product_dict.pop("id")
        return product_dict
