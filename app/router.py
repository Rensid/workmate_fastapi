from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.handler import get_data_from_url
from base import get_async_session


router = APIRouter()


@router.get("/fill_base/")
async def fill_db(session: AsyncSession = Depends(get_async_session)):

    await get_data_from_url(session)


@router.get("/get_last_trading_dates/")
async def get_last_trading_dates(session: AsyncSession = Depends(get_async_session)):
    # список дат последних торговых дней (фильтрация по кол-ву последних торговых дней).
    await view_last_trading_dates(session)


@router.get("/get_dynamics/")
async def get_dynamics(session: AsyncSession = Depends(get_async_session)):
    # список торгов за заданный период (фильтрация по oil_id, delivery_type_id, delivery_basis_id, start_date, end_date).
    pass


@router.get("/get_trading_results/")
async def get_trading_results(session: AsyncSession = Depends(get_async_session)):
    # список последних торгов (фильтрация по oil_id, delivery_type_id, delivery_basis_id)
    pass
