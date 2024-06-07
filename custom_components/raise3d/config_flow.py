"""Adds config flow for Raise3d Integration."""
from __future__ import annotations

import voluptuous as vol
# https://developers.home-assistant.io/docs/development_validation/
import homeassistant.helpers.config_validation as cv
from homeassistant.core import HomeAssistant, callback
from homeassistant import config_entries
from homeassistant.const import (
    CONF_NAME,
    CONF_HOST,
    CONF_SCAN_INTERVAL,
)

from .const import (
    DOMAIN,
    DEFAULT_NAME,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_PORT,
    DEFAULT_IP,
    DEFAULT_PASSWORD,
    CONF_PORT,
    CONF_PASSWORD
)

DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Required(CONF_HOST, default=DEFAULT_IP): cv.string,
        vol.Required(CONF_PORT, default=DEFAULT_PORT): cv.port,
        vol.Required(CONF_PASSWORD, default=DEFAULT_PASSWORD): cv.string,
        vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): cv.positive_int
    }
)

"""Validators and callbacks"""

def host_valid(ip):
    """Return True if hostname or IP address is valid."""
    return True

@callback
def Raise3d_entries(hass: HomeAssistant):
    """Return the hosts already configured."""
    return set(
        entry.data[CONF_HOST] for entry in hass.config_entries.async_entries(DOMAIN)
    )

""" https://developers.home-assistant.io/docs/config_entries_config_flow_handler/
    This handler will manage the creation of entries from user input, discovery or
    other sources (like Home Assistant OS).
"""
class Raise3dFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Raise3D."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    def _host_in_configuration_exists(self, ip) -> bool:
        """Return True if ip exists in configuration."""
        if ip in Raise3d_entries(self.hass):
            return True
        return False



    async def async_step_user(self, user_input: None = None):
        """Handle a flow initialized by the user."""
        errors = {}

        if user_input is not None:
            host = user_input[CONF_HOST]

            if self._host_in_configuration_exists(host):
                errors[CONF_HOST] = "already_configured"
            elif not host_valid(user_input[CONF_HOST]):
                errors[CONF_HOST] = "invalid host address"
            else:
                await self.async_set_unique_id(user_input[CONF_HOST])
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=user_input[CONF_NAME], data=user_input
                )

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )


