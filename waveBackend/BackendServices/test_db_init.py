import requests

API_ships_url = "http://127.0.0.1:8000/ships/"
API_stream_url = "http://127.0.0.1:8000/mqtt-streams/"

ship = {
    "name": "R/V Gunnerus",
    "identifier": "gunnerus",
    "picture_url": "https://www.ntnu.edu/documents/919518/1393991/Gunnerus_starboard_su/8dff7a6a-5645-4972-9327-520a455c4300?t=1282122496969"
}

ship_url = API_ships_url+"1/"

topics = [
    {
        "ship": ship_url,
        "mqtt_path": f"/{ship['identifier']}/total_fuel_consumption"
    },
    {
        "ship": ship_url,
        "mqtt_path": f"/{ship['identifier']}/fuel_level"
    },
    {
        "ship": ship_url,
        "mqtt_path": f"/{ship['identifier']}/fuel_capacity"
    },
    {
        "ship": ship_url,
        "mqtt_path": f"/{ship['identifier']}/speed"
    },
    {
        "ship": ship_url,
        "mqtt_path": f"/{ship['identifier']}/heading"
    },
    {
        "ship": ship_url,
        "mqtt_path": f"/{ship['identifier']}/engine/engine_rpm"
    },
    {
        "ship": ship_url,
        "mqtt_path": f"/{ship['identifier']}/engine/engine_output"
    },
    {
        "ship": ship_url,
        "mqtt_path": f"/{ship['identifier']}/engine/engine_temperature"
    },
    {
        "ship": ship_url,
        "mqtt_path": f"/{ship['identifier']}/engine/engine_fuel_consumption"
    },
    {
        "ship": ship_url,
        "mqtt_path": f"/{ship['identifier']}/generators/generator_1/engine_rpm"
    },
    {
        "ship": ship_url,
        "mqtt_path": f"/{ship['identifier']}/generators/generator_1/engine_output"
    },
    {
        "ship": ship_url,
        "mqtt_path": f"/{ship['identifier']}/generators/generator_1/engine_temperature"
    },
    {
        "ship": ship_url,
        "mqtt_path": f"/{ship['identifier']}/generators/generator_1/engine_fuel_consumption"
    },
    {
        "ship": ship_url,
        "mqtt_path": f"/{ship['identifier']}/generators/generator_2/engine_rpm"
    },
    {
        "ship": ship_url,
        "mqtt_path": f"/{ship['identifier']}/generators/generator_2/engine_output"
    },
    {
        "ship": ship_url,
        "mqtt_path": f"/{ship['identifier']}/generators/generator_2/engine_temperature"
    },
    {
        "ship": ship_url,
        "mqtt_path": f"/{ship['identifier']}/generators/generator_2/engine_fuel_consumption"
    },
]


s = requests.post(API_ships_url, json=ship)
print(s.text)
for t in topics:
    x = requests.post(API_stream_url, json=t)
    print(x.text)

print("-------------------------------------\n"
      "Initial test database setup complete \n"
      "-------------------------------------")
