

from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from models import ExchangeProduct


async def view_last_trading_dates(session: AsyncSession):

    dates = await session.execute(select(ExchangeProduct.date)
                           .order_by(desc(ExchangeProduct.date))
                            .limit(3))
    result = dates.scalars().all()
    print(result)
    
