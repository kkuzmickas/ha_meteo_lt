from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN

# Example list of locations. Replace with the real ones or fetch dynamically.
LOCATIONS = [
    ("location1", "Vilnius"),
    ("location2", "Kaunas"),
    ("location3", "Klaipėda")
]

class SolplanetConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Solplanet."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Save selected location
            return self.async_create_entry(
                title=user_input["location"],
                data=user_input
            )

        # Show dropdown menu
        schema = vol.Schema({
            vol.Required("location"): vol.In({key: name for key, name in LOCATIONS})
        })

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors
        )
