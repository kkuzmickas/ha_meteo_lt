from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.core import HomeAssistant
from .const import DOMAIN, DEFAULT_SCAN_INTERVAL


class MeteoCoordinator(DataUpdateCoordinator):
def __init__(self, hass: HomeAssistant, api):
self.api = api
super().__init__(
hass,
logger=hass.logger,
name="Meteo.lt Coordinator",
update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
)


async def _async_update_data(self):
return await self.api.get_forecast()
