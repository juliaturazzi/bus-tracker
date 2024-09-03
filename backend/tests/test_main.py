import pytest
from temp.app import app
from httpx import AsyncClient
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    return TestClient(app)


@pytest.mark.asyncio
async def test_read_info(client):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(
            "/infos/",
            params={
                "bus_line": "100",
                "start_time": "10:00:00",
                "end_time": "10:30:00",
                "bus_stop": "Barão de Tefé",
            },
        )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert "linha" in response.json()[0]


@pytest.mark.asyncio
async def test_read_info_bus_stop_not_found(client):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(
            "/infos/",
            params={
                "bus_line": "100",
                "start_time": "10:00:00",
                "end_time": "10:30:00",
                "bus_stop": "Invalid Stop",
            },
        )
    assert response.status_code == 404
    assert response.json() == {"detail": "Bus stop not found"}


def test_read_stops(client):
    response = client.get("/stops/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
