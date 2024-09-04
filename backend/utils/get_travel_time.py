import os
from datetime import datetime
from dotenv import load_dotenv
from traveltimepy import Location, Coordinates, TravelTimeSdk, PublicTransport

# load environment variables
load_dotenv()
TRAVEL_TIME_API_ID = os.getenv("TRAVEL_TIME_API_ID")
TRAVEL_TIME_API_KEY = os.getenv("TRAVEL_TIME_API_KEY")


async def get_travel_time(bus_stop_coords, bus_info):
    sdk = TravelTimeSdk(f"{TRAVEL_TIME_API_ID}", f"{TRAVEL_TIME_API_KEY}")

    bus_stop_location = Location(
        id=bus_stop_coords["bus_stop"],
        coords=Coordinates(lat=bus_stop_coords["lat"], lng=bus_stop_coords["lon"]),
    )

    bus_location = Location(
        id=bus_info["ordem"],
        coords=Coordinates(lat=bus_info["latitude"], lng=bus_info["longitude"]),
    )

    result = await sdk.time_filter_async(
        locations=[bus_stop_location, bus_location],
        search_ids={bus_stop_location.id: [bus_location.id]},
        transportation=PublicTransport(type="bus"),
        travel_time=3600,  # max travel time
        departure_time=datetime.now(),
    )

    travel_time = parse_travel_time(result)
    if travel_time:
        return round(travel_time / 60, 2)  # travel time to minutes
    else:
        return "Not found"


def parse_travel_time(result):
    # check if result and locations are available
    if (
        result
        and len(result) > 0
        and hasattr(result[0], "locations")
        and result[0].locations
    ):
        locations = result[0].locations

        # check if locations and properties are available
        if (
            locations
            and len(locations) > 0
            and hasattr(locations[0], "properties")
            and locations[0].properties
        ):
            properties = locations[0].properties

            # check if properties and travel_time are available
            if (
                properties
                and len(properties) > 0
                and hasattr(properties[0], "travel_time")
            ):
                travel_time = properties[0].travel_time
                return travel_time

    return None
