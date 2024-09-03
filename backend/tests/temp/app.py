import pandas as pd
from typing import Dict, Any
from temp.db.create_db import BusStopDatabase
from fastapi import FastAPI, HTTPException
from temp.utils.get_buses_data import get_buses_data
from temp.utils.get_travel_time import get_travel_time
from fastapi.middleware.cors import CORSMiddleware


# initialize FastAPI app
app = FastAPI()

# fixing CORS middleware bug
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# CSV bus stops
STOPS_CSV = "./temp/data/stops_updated.csv"


# load bus stops from CSV
def load_stops():
    df = pd.read_csv(STOPS_CSV)
    df = df[["stop_name", "stop_lat", "stop_lon"]]
    return df


# get coordinates of bus stop by name
def get_stop_coords(stop_name: str):
    stops_df = load_stops()
    stop = stops_df[stops_df["stop_name"] == stop_name]
    if not stop.empty:
        stop_info = stop.iloc[0]
        bus_stops_infos = {
            "bus_stop": stop_info["stop_name"],
            "lat": stop_info["stop_lat"],
            "lon": stop_info["stop_lon"],
        }
        return bus_stops_infos

    raise HTTPException(status_code=404, detail="Bus stop not found")


# filter stops within a radius from coordinate
def parse_stops():
    stops_df = load_stops()
    filtered_stops = []

    for _, row in stops_df.iterrows():
        filtered_stops.append(row.to_dict())

    return filtered_stops


# parse coordinates from string to float
def parse_coords(coord: str):
    return float(coord.replace(",", "."))


# get user filtered bus lines
async def get_filtered_bus_line(bus_line, start_time, end_time, bus_stop_name):
    bus_stop_coords = get_stop_coords(bus_stop_name)
    buses_data = get_buses_data(start_time, end_time)

    if bus_line is not None:
        seen_ordem = set()
        filtered_bus_line = []

        for line_data in buses_data:
            if (
                line_data["linha"] == str(bus_line)
                and line_data["ordem"] not in seen_ordem
                and not seen_ordem.add(line_data["ordem"])
            ):
                bus_info = {
                    "linha": line_data.get("linha"),
                    "velocidade": line_data.get("velocidade"),
                    "latitude": parse_coords(line_data.get("latitude")),
                    "longitude": parse_coords(line_data.get("longitude")),
                    "ordem": line_data.get("ordem"),
                }

                travel_time = await get_travel_time(
                    bus_stop_coords, bus_info, start_time
                )

                bus_info["distancia"] = travel_time
                filtered_bus_line.append(bus_info)

    else:
        filtered_bus_line = buses_data

    return filtered_bus_line


# get bus lines information
@app.get("/infos/")
async def read_info(bus_line: str, start_time: str, end_time: str, bus_stop: str):
    return await get_filtered_bus_line(bus_line, start_time, end_time, bus_stop)


# get bus stops within a radius coordinates
@app.get("/stops/")
def read_stops():
    return parse_stops()


@app.post("/register/")
async def send_email_endpoint(data: Dict[Any, Any]):
    bus_stop_info = get_stop_coords(data["bus_stop"])
    bus_stop_name = data["bus_stop"]
    bus_line = data["bus_line"]
    lat = bus_stop_info["lat"]
    lon = bus_stop_info["lon"]
    start_time = data["start_time"]
    end_time = data["end_time"]
    email = data["email"]
    db = BusStopDatabase()
    db.insert_bus_stop(email, bus_line, bus_stop_name, lat, lon, start_time, end_time)
    return {"status": "success", "message": "Email sent successfully"}
