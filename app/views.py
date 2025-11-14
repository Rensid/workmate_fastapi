from sqlalchemy import and_, desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.schema import ExchangeProductFilter
from models import ExchangeProduct


async def view_last_trading_dates(session: AsyncSession):
    dates = await session.execute(
        select(ExchangeProduct.date).order_by(desc(ExchangeProduct.date)).limit(3)
    )
    result = dates.scalars().all()
    return result


async def view_get_dynamics(
    product: ExchangeProductFilter, start_date, end_date, session: AsyncSession
):
    statements = []

    if product.oil_id is not None:
        statements.append(ExchangeProduct.oil_id == product.oil_id)
    if product.delivery_basis_id is not None:
        statements.append(
            ExchangeProduct.delivery_basis_id == product.delivery_basis_id
        )
    if product.delivery_type_id is not None:
        statements.append(ExchangeProduct.delivery_type_id == product.delivery_type_id)

    if start_date and end_date:
        statements.append(ExchangeProduct.date.between(start_date, end_date))

    query = select(ExchangeProduct)
    if statements:
        query = query.filter(and_(*statements))

    result = await session.execute(query)
    return result.scalars().all()


async def view_trading_results(product: ExchangeProductFilter, session: AsyncSession):
    statements = []

    if product.oil_id is not None:
        statements.append(ExchangeProduct.oil_id == product.oil_id)
    if product.delivery_basis_id is not None:
        statements.append(
            ExchangeProduct.delivery_basis_id == product.delivery_basis_id
        )
    if product.delivery_type_id is not None:
        statements.append(ExchangeProduct.delivery_type_id == product.delivery_type_id)

    query = select(ExchangeProduct)
    if statements:
        query = (
            query.filter(and_(*statements))
            .order_by(desc(ExchangeProduct.date))
            .limit(3)
        )

    result = await session.execute(query)
    return result.scalars().all()
