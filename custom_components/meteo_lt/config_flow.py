import aiohttp
import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN

LOCATIONS_URL = "https://api.meteo.lt/v1/places"

class MeteoLtConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for meteo.lt."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            return self.async_create_entry(
                title=user_input["location_name"],
                data=user_input
            )

        # Fetch locations dynamically
        locations = await self._fetch_locations()
        if not locations:
            errors["base"] = "cannot_connect"
            options = {}
        else:
            options = {loc["id"]: loc["name"] for loc in locations}

        schema = vol.Schema({
            vol.Required("location_id"): vol.In(options)
        })

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors
        )

    async def _fetch_locations(self):
        """Fetch available locations from meteo.lt API."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(LOCATIONS_URL, timeout=10) as resp:
                    if resp.status != 200:
                        return None
                    return await resp.json()
        except Exception:
            return None
