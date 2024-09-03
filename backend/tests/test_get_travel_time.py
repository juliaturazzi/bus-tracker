import pytest
from datetime import datetime
from unittest.mock import AsyncMock, patch
from temp.utils.get_travel_time import get_travel_time

start_time = datetime.now()


@pytest.mark.asyncio
@patch("temp.utils.get_travel_time.TravelTimeSdk")
async def test_get_travel_time_no_travel_time(mock_sdk):
    bus_stop_coords = {"bus_stop": "Central", "lat": -22.9068, "lon": -43.1729}
    bus_info = {"ordem": "1001", "latitude": -22.9068, "longitude": -43.1729}

    mock_result = [
        {"locations": [{"id": "Central", "properties": [{"travel_time": None}]}]}
    ]
    mock_sdk.return_value.time_filter_async = AsyncMock(return_value=mock_result)

    travel_time = await get_travel_time(bus_stop_coords, bus_info, start_time)

    assert travel_time == "Not found"


@pytest.mark.asyncio
@patch("temp.utils.get_travel_time.TravelTimeSdk")
async def test_get_travel_time_api_failure(mock_sdk):
    bus_stop_coords = {"bus_stop": "Central", "lat": -22.9068, "lon": -43.1729}
    bus_info = {"ordem": "1001", "latitude": -22.9068, "longitude": -43.1729}

    mock_sdk.return_value.time_filter_async = AsyncMock(
        side_effect=Exception("API error")
    )

    with pytest.raises(Exception, match="API error"):
        await get_travel_time(bus_stop_coords, bus_info, start_time)
