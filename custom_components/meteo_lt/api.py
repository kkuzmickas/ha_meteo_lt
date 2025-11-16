import aiohttp
import async_timeout


class MeteoLTApi:
def __init__(self, session: aiohttp.ClientSession, place: str):
self.session = session
self.place = place


async def get_places(self):
url = "https://api.meteo.lt/v1/places"
async with async_timeout.timeout(30):
async with self.session.get(url) as resp:
return await resp.json()


async def get_forecast(self):
url = f"https://api.meteo.lt/v1/places/{self.place}/forecasts/long-term"
async with async_timeout.timeout(30):
async with self.session.get(url) as resp:
return await resp.json()
