from typing import List
from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession

from app.handler import get_data_from_url
from app.schema import ExchangeProductAll, ExchangeProductFilter
from app.views import view_get_dynamics, view_last_trading_dates, view_trading_results
from base import get_async_session


router = APIRouter()


@router.get("/fill_base/")
@cache()
async def fill_db(session: AsyncSession = Depends(get_async_session)):
    await get_data_from_url(session)


@router.get("/get_last_trading_dates/")
@cache()
async def get_last_trading_dates(session: AsyncSession = Depends(get_async_session)):
    # список дат последних торговых дней (фильтрация по кол-ву последних торговых дней).
    result = await view_last_trading_dates(session)
    return result


@router.get("/get_dynamics/", response_model=List[ExchangeProductAll])
@cache()
async def get_dynamics(
    product: ExchangeProductFilter,
    start_date: date,
    end_date: date,
    session: AsyncSession = Depends(get_async_session),
):
    # список торгов за заданный период (фильтрация по oil_id, delivery_type_id, delivery_basis_id, start_date, end_date).
    result = await view_get_dynamics(product, start_date, end_date, session)
    return result


@router.get("/get_trading_results/", response_model=List[ExchangeProductAll])
@cache()
async def get_trading_results(
    product: ExchangeProductFilter, session: AsyncSession = Depends(get_async_session)
):
    # список последних торгов (фильтрация по oil_id, delivery_type_id, delivery_basis_id)
    result = await view_trading_results(product, session)

    return result
