from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .const import DOMAIN
from .api import MeteoLTApi
from .coordinator import MeteoCoordinator


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
session = async_get_clientsession(hass)
api = MeteoLTApi(session, entry.data["place"])


coordinator = MeteoCoordinator(hass, api)
await coordinator.async_config_entry_first_refresh()


hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator


await hass.config_entries.async_forward_entry_setups(entry, ["weather"])
return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
unload_ok = await hass.config_entries.async_forward_entry_unload(entry, "weather")
if unload_ok:
hass.data[DOMAIN].pop(entry.entry_id)
return unload_ok
