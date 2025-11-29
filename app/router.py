from typing import Annotated, List
from fastapi import APIRouter, Depends
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession

from app.decorators.cache_decorator import cache
from app.parser.handler import get_data_from_url
from app.schema import ExchangeProductAll, ExchangeProductFilter
from app.views import view_get_dynamics, view_last_trading_dates, view_trading_results
from base import get_async_session


router = APIRouter()


@router.get("/fill_base/")
async def fill_db():
    await get_data_from_url()


@router.get("/get_last_trading_dates")
@cache
async def get_last_trading_dates(session: AsyncSession = Depends(get_async_session)):
    result = await view_last_trading_dates(session)
    return result


@router.get("/get_dynamics", response_model=List[ExchangeProductAll])
@cache
async def get_dynamics(
    start_date: date,
    end_date: date,
    product: Annotated[ExchangeProductFilter, Depends()],
    session: AsyncSession = Depends(get_async_session),
):
    result = await view_get_dynamics(product, start_date, end_date, session)
    return result


@router.get("/get_trading_results", response_model=List[ExchangeProductAll])
@cache
async def get_trading_results(
    product: Annotated[ExchangeProductFilter, Depends()],
    session: AsyncSession = Depends(get_async_session),
):
    result = await view_trading_results(product, session)

    return result
