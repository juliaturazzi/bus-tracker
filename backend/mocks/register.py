import requests

register_url = "http://localhost:8000/register/"
register_data = {
    "email": "teste123@gmail.com",
    "username": "teste",
    "password": "melusca",
}
headers = {"Content-Type": "application/json"}

response = requests.post(register_url, json=register_data, headers=headers)

token_url = "http://localhost:8000/token"
token_data = {"username": "teste123@gmail.com", "password": "melusca"}
headers = {"Content-Type": "application/x-www-form-urlencoded"}

response = requests.post(token_url, data=token_data, headers=headers)
token_response = response.json()

access_token = token_response.get("access_token")
if not access_token:
    raise ValueError("Failed to retrieve access token.")

stops_register_url = "http://localhost:8000/stops/register/"
stops_data = {
    "bus_line": "123",
    "stop_name": "Central Station",
    "latitude": -22.912,
    "longitude": -43.230,
    "start_time": "08:00:00",
    "end_time": "09:00:00",
}
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json",
}

response = requests.post(stops_register_url, json=stops_data, headers=headers)
