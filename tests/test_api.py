from httpx import ASGITransport, AsyncClient
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.schema import ExchangeProductFilter
from base import get_async_session
from tests.test_base import get_test_async_session, run_migrations


client = TestClient(app=app)


app.dependency_overrides[get_async_session] = get_test_async_session


@pytest.mark.anyio
@pytest.mark.parametrize(
    "start_date, end_date, product, result",
    [
        (
            "2025-11-23",
            "2025-11-28",
            ExchangeProductFilter("A106", "PDK", "J"),
            [
                {
                    "oil_id": "A106",
                    "delivery_basis_id": "PDK",
                    "delivery_type_id": "J",
                    "delivery_basis_name": "Предкомбинатская-группа станций",
                    "exchange_product_id": "A106PDK060J",
                    "exchange_product_name": "Бензин (АИ-100-К5) EURO-6, Предкомбинатская-группа станций (ст. отправления ОТП)",
                    "volume": 60.0,
                    "total": 5514420.0,
                    "count": 1,
                }
            ],
        ),
        ("2025-11-23", "2025-11-23", ExchangeProductFilter("A692", "PDK", "J"), []),
    ],
)
async def test_get_last_trading_dates(start_date, end_date, product, result):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost"
    ) as ac:
        params = {
            "start_date": start_date,
            "end_date": end_date,
            "oil_id": product.oil_id,
            "delivery_basis_id": product.delivery_basis_id,
            "delivery_type_id": product.delivery_type_id,
        }
        response = await ac.get("/get_last_trading_dates/", params=params)
        assert response.status_code == 200
        assert response.json() == result
