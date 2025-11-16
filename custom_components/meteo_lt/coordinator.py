from datetime import timedelta
import aiohttp
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .const import WEATHER_URL, CONF_LOCATION_ID

class MeteoLtDataUpdateCoordinator(DataUpdateCoordinator):
    """Coordinator to fetch weather data from meteo.lt"""

    def __init__(self, hass, config):
        self.hass = hass
        self.location_id = config[CONF_LOCATION_ID]
        super().__init__(
            hass,
            _LOGGER := hass.logger,
            name="Meteo.lt Weather",
            update_interval=timedelta(minutes=30),
        )

    async def _async_update_data(self):
        try:
            url = WEATHER_URL.format(location_id=self.location_id)
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as resp:
                    if resp.status != 200:
                        raise UpdateFailed(f"HTTP error {resp.status}")
                    return await resp.json()
        except Exception as err:
            raise UpdateFailed(f"Error fetching data: {err}")
