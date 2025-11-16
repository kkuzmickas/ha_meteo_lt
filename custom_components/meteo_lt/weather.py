from homeassistant.components.weather import WeatherEntity, WeatherEntityFeature
from homeassistant.const import TEMP_CELSIUS
from .const import DOMAIN


MAP = {
"clear": "sunny",
"partly-cloudy": "partlycloudy",
"cloudy": "cloudy",
"cloudy-with-sunny-intervals": "partlycloudy",
"rain": "rainy",
"light-rain": "rainy",
"sleet": "snowy-rainy",
"snow": "snowy",
"fog": "fog",
"thunderstorms": "lightning"
}


async def async_setup_entry(hass, entry, async_add_entities):
coordinator = hass.data[DOMAIN][entry.entry_id]
async_add_entities([MeteoWeather(coordinator)])


class MeteoWeather(WeatherEntity):
_attr_native_temperature_unit = TEMP_CELSIUS
_attr_supported_features = WeatherEntityFeature.FORECAST_HOURLY


def __init__(self, coordinator):
self.coordinator = coordinator


@property
def name(self):
return "Meteo.lt Weather"


@property
def native_temperature(self):
return self._now()["airTemperature"]


@property
def condition(self):
return MAP.get(self._now()["conditionCode"], "cloudy")


def _now(self):
data = self.coordinator.data["forecastTimestamps"]
return data[0]


@property
def forecast(self):
return [
{
"datetime": ts["forecastTimeUtc"],
"temperature": ts["airTemperature"],
"condition": MAP.get(ts["conditionCode"], "cloudy"),
}
for ts in self.coordinator.data["forecastTimestamps"][:24]
]


async def async_update(self):
await self.coordinator.async_request_refresh()
