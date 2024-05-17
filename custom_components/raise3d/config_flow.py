"""Adds config flow for Raise3dEntity."""
from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_create_clientsession
from homeassistant.const import (
    CONF_NAME, 
    CONF_USERNAME,
)

from .api import (
    Raise3dClient,
    Raise3dClientAuthenticationError,
    Raise3dClientCommunicationError,
    Raise3dClientError,
)

from .const import DOMAIN, LOGGER

""" https://developers.home-assistant.io/docs/config_entries_config_flow_handler/
    This handler will manage the creation of entries from user input, discovery or 
    other sources (like Home Assistant OS).
"""
class Raise3dFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Raise3D"""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> config_entries.FlowResult:
        """Handle a flow initialized by the user."""
        _errors = {}
        if user_input is not None:
            try:
                await self._test_credentials(
                    username=user_input[CONF_USERNAME],
                    password=user_input[CONF_PASSWORD],
                )
            except Raise3dClientAuthenticationError as exception:
                LOGGER.warning(exception)
                _errors["base"] = "auth"
            except Raise3dClientCommunicationError as exception:
                LOGGER.error(exception)
                _errors["base"] = "connection"
            except Raise3dClientError as exception:
                LOGGER.exception(exception)
                _errors["base"] = "unknown"
            else:
                return self.async_create_entry(
                    title=user_input[CONF_USERNAME],
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_USERNAME,
                        default=(user_input or {}).get(CONF_USERNAME),
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.TEXT
                        ),
                    ),
                    vol.Required(CONF_PASSWORD): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.PASSWORD
                        ),
                    ),
                }
            ),
            errors=_errors,
        )

    async def _test_credentials(self, username: str, password: str) -> None:
        """Validate credentials."""
        client = Raise3dClient(
            username=username,
            password=password,
            session=async_create_clientsession(self.hass),
        )
        await client.async_get_data()
