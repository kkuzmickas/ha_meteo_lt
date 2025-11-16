from homeassistant.helpers.entity import Entity
from .const import DOMAIN, API_BASE
import requests

class MeteoLtSensor(Entity):
    def __init__(self, location):
        self._location = location
        self._state = None
        self._attributes = {}

    @property
    def name(self):
        return f"Meteo LT {self._location}"

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attributes

    def update(self):
        # Fetch weather data
        url = f"{API_BASE}/places/{self._location}/forecasts/long-term"
        response = requests.get(url)
        if response.ok:
            data = response.json()
            self._state = data.get("forecastTimestamps")[0]["airTemperature"]
            self._attributes = {
                "condition": data.get("forecastTimestamps")[0]["conditionCode"],
                "windSpeed": data.get("forecastTimestamps")[0]["windSpeed"]
            }
