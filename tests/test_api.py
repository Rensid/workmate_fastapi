from httpx import ASGITransport, AsyncClient
import pytest
from fastapi.testclient import TestClient
from app.main import app
from base import get_async_session
from tests.test_base import get_test_async_session, run_migrations


client = TestClient(app=app)


app.dependency_overrides[get_async_session] = get_test_async_session


@pytest.mark.anyio
async def test_get_last_trading_dates(run_migrations):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost:8000"
    ) as ac:
        response = ac.get("/get_last_trading_dates/")
        assert response.status_code == "200"
