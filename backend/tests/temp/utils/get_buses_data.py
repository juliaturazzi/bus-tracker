import requests
from datetime import datetime

# bus data API URL
BUS_API_URL = "https://dados.mobilidade.rio/gps/sppo?"


# fetch bus data from the API for a specified time range.
def get_buses_data(start_time: str, end_time: str):

    today = datetime.now().strftime("%d-%m-%Y")
    start_time = today + "+" + str(start_time)
    end_time = today + "+" + str(end_time)

    # API query URL with the time range
    date_query = f"{BUS_API_URL}dataInicial={start_time}&dataFinal={end_time}"
    print(f"Bus query: {date_query}")

    buses_data = requests.get(date_query).json()  # return data as JSON
    print(f"Buses data len -> {len(buses_data)}")

    return buses_data
