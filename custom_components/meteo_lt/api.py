import aiohttp

BASE = "https://api.meteo.lt/v1"

class MeteoLTApi:
    def __init__(self, session, place_code):
        self._session = session
        self.place = place_code

    async def get_forecast(self):
        url = f"{BASE}/places/{self.place}/forecasts/long-term"
        async with self._session.get(url) as resp:
            return await resp.json()

    async def get_places(self):
        async with self._session.get(f"{BASE}/places") as resp:
            return await resp.json()
