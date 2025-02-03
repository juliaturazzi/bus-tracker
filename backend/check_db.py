import asyncio
from datetime import datetime
from collections import defaultdict, deque

from dotenv import load_dotenv
import sys

from app import get_filtered_bus_line
from db.create_db import BusStopDatabase
from services.email_service import send_email
from services.travel_time_service import TravelTimeService

load_dotenv()

NEARBY_BUSES_MINUTES_MIN = 0
NEARBY_BUSES_MINUTES_MAX = 11.00

bus_positions = defaultdict(lambda: deque(maxlen=2))


def check_time(start, end):
    current_time = datetime.now().time()

    if end < start:
        result = current_time >= start or current_time < end
    else:
        result = start <= current_time < end

    return result


def stop_to_dict(stop):
    stop_dict = stop
    start_time = str(stop.get("start_time"))
    end_time = str(stop.get("end_time"))
    stop_dict["start_time"] = datetime.strptime(start_time, "%H:%M:%S").time()
    stop_dict["end_time"] = datetime.strptime(end_time, "%H:%M:%S").time()
    return stop_dict


async def evaluate_travel_time(stop, buses, service):
    bus_stop_info = {
        "bus_stop": stop["stop_name"],
        "lat": stop["latitude"],
        "lon": stop["longitude"],
    }

    updated_buses = await asyncio.to_thread(
        service.get_travel_times, bus_stop_info, buses
    )
    return updated_buses


async def collect_bus_data(stop, buses, service):
    bus_data = {}
    updated_buses = await evaluate_travel_time(stop, buses, service)
    for bus in updated_buses:
        distancia = bus.get("distancia")
        max_distance = stop.get("max_distance")
        bus_id = bus.get("id") or bus.get("ordem")

        if distancia != "Not found" and bus_id:
            try:
                current_distance = float(distancia)
            except ValueError:
                continue

            if 0 <= current_distance < max_distance:
                previous_distances = bus_positions[bus_id]
                is_approaching = False
                if len(previous_distances) == 2:
                    if (
                        previous_distances[0] > previous_distances[1]
                        and previous_distances[1] > current_distance
                    ):
                        is_approaching = True
                elif len(previous_distances) == 1:
                    if previous_distances[0] > current_distance:
                        is_approaching = True
                else:
                    is_approaching = True

                if is_approaching:
                    bus_data[bus_id] = distancia

                bus_positions[bus_id].append(current_distance)

    return bus_data


async def process_stop(stop, service):
    if check_time(stop["start_time"], stop["end_time"]):
        buses = await get_filtered_bus_line(
            stop["linha"],
            stop["start_time"],
            stop["end_time"],
            stop["stop_name"],
        )
        if not buses:
            return
        bus_data = await collect_bus_data(stop, buses, service)
        if bus_data:
            await asyncio.to_thread(
                send_email, stop["email"], stop["linha"], stop["stop_name"], bus_data
            )


def process_all_bus_stops():
    db = BusStopDatabase()
    raw_stops = db.get_all_bus_stops()
    if raw_stops:
        for raw_stop in raw_stops:
            stop = stop_to_dict(raw_stop)
            yield stop


async def main():
    service = TravelTimeService()
    while True:
        tasks = []
        for stop in process_all_bus_stops():
            tasks.append(process_stop(stop, service))
        if tasks:
            await asyncio.gather(*tasks)
        await asyncio.sleep(60)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(e)
