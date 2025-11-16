from homeassistant.components.weather import (
    WeatherEntity,
    WeatherEntityFeature,
)
from homeassistant.const import TEMP_CELSIUS
from .const import DOMAIN

ASCII_MAP = {
    "clear": "sunny",
    "cloudy": "cloudy",
    "rain": "rainy",
    "snow": "snowy",
    "fog": "fog",
}

async def async_setup_entry(hass, entry, async_add_entities):
    api = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([MeteoLTWeather(api)])

class MeteoLTWeather(WeatherEntity):
    _attr_name = "Meteo.lt Weather"
    _attr_native_temperature_unit = TEMP_CELSIUS
    _attr_supported_features = WeatherEntityFeature.FORECAST_HOURLY

    def __init__(self, api):
        self.api = api
        self.data = None

    async def async_update(self):
        self.data = await self.api.get_forecast()

    @property
    def native_temperature(self):
        return self.data["forecastTimestamps"][0]["airTemperature"]

    @property
    def condition(self):
        code = self.data["forecastTimestamps"][0]["conditionCode"]
        return ASCII_MAP.get(code, "cloudy")

    @property
    def forecast(self):
        return [
            {
                "datetime": ts["forecastTimeUtc"],
                "temperature": ts["airTemperature"],
                "condition": ASCII_MAP.get(ts["conditionCode"], "cloudy")
            }
            for ts in self.data["forecastTimestamps"][:24]
        ]
