import requests
from modules.common_types import Coordinate
import aiohttp


def fetch_elevation(coordinates: list[Coordinate]) -> list[int]:
    url = "https://maps.vk.com/api/elevation?api_key="  # Replace with the actual URL

    coordinates_list = [{"lat":coordinate.lat, "lon":coordinate.lon} for coordinate in coordinates]

    payload = {"locations": coordinates_list}
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        data = response.json()
        heights = data.get('height') # we've got only one height value
        return [height for height in heights if height is not None]

    print(f"Failed to fetch elevation data. Status code: {response.status_code}")
    return None

async def async_fetch_elevation(session: aiohttp.ClientSession,coordinates: list[Coordinate]) -> list[int]:

    url = "https://maps.vk.com/api/elevation?api_key="  # Replace with the actual URL

    coordinates_list = [{"lat": coordinate.lat, "lon": coordinate.lon} for coordinate in coordinates]

    payload = {"locations": coordinates_list}
    async with session.post(url, json=payload) as response:
        if response.status == 200:
            data = await response.json()
            heights = data.get('height')  # we've got only one height value
            return [height for height in heights if height is not None]

        print(f"Failed to fetch elevation data. Status code: {response.status}")
        return None