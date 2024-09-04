import time
import asyncio
from datetime import datetime
from app import get_filtered_bus_line
from db.create_db import BusStopDatabase
from services.email_service import send_email
from utils.get_travel_time import get_travel_time
from dotenv import load_dotenv

load_dotenv()

# ten minute range
NEARBY_BUSES_MINUTES_MIN = 0
NEARBY_BUSES_MINUTES_MAX = 11.00


# check if the current time is within a specified interval
def check_time(start, end):
    current_time = datetime.now().time()

    # if end time is before start time, the interval crosses midnight
    if end < start:
        return current_time >= start or current_time < end
    else:
        return start <= current_time < end


# evaluate travel time to a bus stop
async def evaluate_travel_time(stop, bus):
    bus_stop_info = {
        "bus_stop": stop["stop_name"],
        "lat": stop["lat"],
        "lon": stop["lon"],
    }

    travel_time = await get_travel_time(bus_stop_info, bus)
    return travel_time


# convert stop data to a dictionary
def stop_to_dict(stop):
    start_time = str(stop[5])
    end_time = str(stop[6])
    return {
        "email": stop[0],
        "bus_line": stop[1],
        "stop_name": stop[2],
        "lat": stop[3],
        "lon": stop[4],
        "start_time": (datetime.strptime(start_time, "%H:%M:%S").time()),
        "end_time": (datetime.strptime(end_time, "%H:%M:%S").time()),
    }


# check and evaluate travel times
async def main():
    while True:
        db = BusStopDatabase()
        raw_stops = db.get_all_bus_stops()
        if raw_stops is not None:
            for raw_stop in raw_stops:
                stop = stop_to_dict(raw_stop)

                if check_time(stop["start_time"], stop["end_time"]):
                    buses = await get_filtered_bus_line(
                        stop["bus_line"],
                        stop["start_time"],
                        stop["end_time"],
                        stop["stop_name"],
                    )

                    bus_data = {}

                    for bus in buses:
                        travel_time = await evaluate_travel_time(stop, bus)
                        if travel_time != "Not found":
                            if (
                                NEARBY_BUSES_MINUTES_MIN
                                <= float(travel_time)
                                < NEARBY_BUSES_MINUTES_MAX
                            ):
                                bus_data[bus["ordem"]] = travel_time

                    if bus_data:
                        send_email(
                            stop["email"], stop["bus_line"], stop["stop_name"], bus_data
                        )
                else:
                    continue

        time.sleep(60)  # check and try to send an e-mail every minute


if __name__ == "__main__":
    asyncio.run(main())
