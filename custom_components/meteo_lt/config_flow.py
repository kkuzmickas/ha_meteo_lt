from homeassistant import config_entries
from .const import DOMAIN, API_BASE
import requests

class MeteoLtConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        locations = self._get_locations()
        if user_input is not None:
            return self.async_create_entry(title=user_input["location"], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=self._generate_schema(locations)
        )

    def _get_locations(self):
        response = requests.get(f"{API_BASE}/places")
        if response.ok:
            return [loc["code"] for loc in response.json()]
        return []

    def _generate_schema(self, locations):
        import voluptuous as vol
        from homeassistant.helpers import config_validation as cv
        return vol.Schema({
            vol.Required("location"): vol.In(locations)
        })
