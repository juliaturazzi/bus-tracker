import requests
from datetime import datetime
from json import dumps


class BusDataFetcher:
    BASE_API_URL = "https://dados.mobilidade.rio/gps/sppo?"

    def __init__(self):
        self.today = datetime.now().strftime("%d-%m-%Y")

    def get_buses_data(self, start_time: str, end_time: str):
        formatted_start_time = f"{self.today}+{start_time}"
        formatted_end_time = f"{self.today}+{end_time}"
        date_query = f"{self.BASE_API_URL}dataInicial={formatted_start_time}&dataFinal={formatted_end_time}"

        try:
            response = requests.get(date_query)
            response.raise_for_status()

            data = response.json()
            if not isinstance(data, list):
                return []

            return data
        except ValueError as ve:            
            return ve
        except requests.RequestException as e:
            return e


if __name__ == "__main__":
    fetcher = BusDataFetcher()
    data = fetcher.get_buses_data("10:00:00", "11:00:00")
