"""Custom integration for Raise3D printers with Home Assistant."""

from __future__ import annotations
import asyncio
import logging
import threading
from datetime import timedelta
from typing import Optional
import json
import urllib

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME, CONF_HOST, CONF_SCAN_INTERVAL
from homeassistant.core import HomeAssistant
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.event import async_track_time_interval

import voluptuous as vol

from .const import (
    DOMAIN,
    DEFAULT_IP,
    DEFAULT_NAME,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_PORT
)

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.SWITCH,
]


# https://developers.home-assistant.io/docs/config_entries_index/#setting-up-an-entry
async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up this integration using UI."""
    host = entry.data[CONF_HOST]
    name = entry.data[CONF_NAME]
    scan_interval = entry.data[CONF_SCAN_INTERVAL]

    _LOGGER.debug("Setup Pellematic Hub %s, %s", DOMAIN, name)

    hub = PellematicHub(hass, name, host, scan_interval)

    # Register the hub.
    hass.data[DOMAIN][name] = {"hub": hub}

    for component in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, component)
        )
    return Tru


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle removal of an entry."""
    if unloaded := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    return unloaded


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)


class Raise3dHub:
    """Thread safe wrapper class."""

    def __init__(
        self,
        hass: HomeAssistant,
        name,
        host,
        scan_interval,
    ) -> None:
        """Initialize the hub."""
        self._hass = hass
        self._host = host
        self._lock = threading.Lock()
        self._name = name
        self._scan_interval = timedelta(seconds=scan_interval)
        self._unsub_interval_method = None
        self._sensors = []
        self.data = {}

    @callback
    def async_add_raise3d_sensor(self, update_callback):
        """Listen for data updates."""
        # This is the first sensor, set up interval.
        if not self._sensors:
            self._unsub_interval_method = async_track_time_interval(
                self._hass, self.async_refresh_api_data, self._scan_interval
            )

        self._sensors.append(update_callback)

    @callback
    def async_remove_raise3d_sensor(self, update_callback):
        """Remove data update."""
        self._sensors.remove(update_callback)

        if not self._sensors:
            # stop the interval timer upon removal of last sensor.
            self._unsub_interval_method()
            self._unsub_interval_method = None

    async def async_refresh_api_data(self, _now: Optional[int] = None) -> None:
        """Time to update."""
        if not self._sensors:
            return

        try:
            update_result = await self.fetch_raise3d_data()
        except Exception as e:
            _LOGGER.exception("Error reading raise3d data")
            update_result = False

        if update_result:
            for update_callback in self._sensors:
                update_callback()

    @property
    def name(self):
        """Return the name of this hub."""
        return self._name

    async def fetch_raise3d_data(self):
        """Get data from api"""
        result = await self._hass.async_add_executor_job(fetch_data, self._host)
        self.data = result
        return True


def fetch_data(url: str):
    """Get data"""
    # _LOGGER.debug("Fetching raise3d datas with REST API")

    req = urllib.request.Request(url)
    response = None
    str_response = None
    try:
        response = urllib.request.urlopen(
            req, timeout=3
        )  # okofen api recommanded timeout is 2,5s
        str_response = response.read().decode("iso-8859-1", "ignore")
    finally:
        if response is not None:
            response.close()

    # Hotfix for raise3d update 4.02 (invalid json)
    str_response = str_response.replace("L_statetext:", 'L_statetext":')
    result = json.loads(str_response, strict=False)
    return result




