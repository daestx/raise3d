"""Adds config flow for Raise3dEntity."""
from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_create_clientsession
from homeassistant.const import (
    CONF_NAME,
    CONF_IP_ADDRESS,
    CONF_SCAN_INTERVAL,
)

from .const import (
    DOMAIN,
    DEFAULT_NAME,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_PORT,
    DEFAULT_IP,
    CONF_PORT,
    CONF_IP
)

DATA_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): str,
        vol.Optional(CONF_IP, default=DEFAULT_IP): str,
        vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): int,
        vol.Optional(CONF_PORT, default=DEFAULT_PORT): int
    }
)


""" https://developers.home-assistant.io/docs/config_entries_config_flow_handler/
    This handler will manage the creation of entries from user input, discovery or 
    other sources (like Home Assistant OS).
"""

@callback
def Raise3d_entries(hass: HomeAssistant):
    """Return the hosts already configured."""
    return set(
        entry.data[CONF_IP_ADDRESS] for entry in hass.config_entries.async_entries(DOMAIN)
    )

class Raise3dFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Raise3D"""

    VERSION = 1

    def _ip_in_configuration_exists(self, ip) -> bool:
        """Return True if ip exists in configuration."""
        if ip in Raise3d_entries(self.hass):
            return True
        return False



    async def async_step_user(self, user_input: None = None):
        """Handle a flow initialized by the user."""
        _errors = {}
        if user_input is not None:
            host = user_input[CONF_IP_ADDRESS]

            if self._host_in_configuration_exists(host):
                errors[CONF_IP_ADDRESS] = "already_configured"
            elif not host_valid(user_input[CONF_IP_ADDRESS]):
                errors[CONF_IP_ADDRESS] = "invalid ip address"
            else:
                await self.async_set_unique_id(user_input[CONF_IP_ADDRESS])
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=user_input[CONF_NAME], data=user_input
                )

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=_errors
        )


