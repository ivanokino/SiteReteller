from httpx import AsyncClient, ASGITransport
import pytest
from main import app
from Database.history_database import setup_db

@pytest.mark.asyncio
async def test_root():
    async with AsyncClient(transport=ASGITransport(app=app),
                           base_url="http://test") as ac:
        response = await ac.get("/")

    assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_retell():
    await setup_db()
    async with AsyncClient(transport=ASGITransport(app=app),
                           base_url="http://test") as ac:
        response = await ac.get("/retell?url=https://www.youtube.com/")

    assert response.status_code == 200

@pytest.mark.asyncio
async def test_del_history():
    await setup_db()
    async with AsyncClient(transport=ASGITransport(app=app),
        base_url="http://test") as ac:

        response = await ac.post("/history")

    assert response.status_code == 200  

@pytest.mark.asyncio
async def test_getl_history():
    await setup_db()
    async with AsyncClient(transport=ASGITransport(app=app),
        base_url="http://test") as ac:

        response = await ac.get("/history")

    assert response.status_code == 200  
