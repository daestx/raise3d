"""Custom integration for Raise3D printers with Home Assistant."""

from __future__ import annotations
from .const import (
    DOMAIN,
    DEFAULT_IP,
    DEFAULT_NAME,
    DEFAULT_SCAN_INTERVAL,
    CONF_PORT,
    CONF_PASSWORD
)
import asyncio
import logging
import threading
from datetime import timedelta
from typing import Optional

import homeassistant.helpers.config_validation as cv
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME, CONF_HOST, CONF_SCAN_INTERVAL
from homeassistant.core import HomeAssistant
from homeassistant.core import callback
# from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.event import async_track_time_interval

import voluptuous as vol
import custom_components.raise3d.raise_api as r3d


_LOGGER = logging.getLogger(__name__)

RAISE3D_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Optional(CONF_HOST, default=DEFAULT_IP): cv.string,
        vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): cv.positive_int,
    }
)

CONFIG_SCHEMA = vol.Schema(
    {DOMAIN: vol.Schema({cv.slug: RAISE3D_SCHEMA})}, extra=vol.ALLOW_EXTRA
)

PLATFORMS = ["sensor"]


async def async_setup(hass: HomeAssistant, config):
    """Set up the Rgaise3D component."""
    hass.data[DOMAIN] = {}
    return True


# https://developers.home-assistant.io/docs/config_entries_index/#setting-up-an-entry
async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up this integration using UI."""
    host = entry.data[CONF_HOST]
    name = entry.data[CONF_NAME]
    scan_interval = entry.data[CONF_SCAN_INTERVAL]
    port = entry.data[CONF_PORT]
    password = entry.data[CONF_PASSWORD]

    _LOGGER.debug("Setup Raise3d Hub: domain:%s, name:%s", DOMAIN, name)
    _LOGGER.debug("Setup Raise3d Hub: password:%s, port:%s, scan_interval:%s",
                  password, port, scan_interval)

    hub = Raise3dHub(hass, name, host, scan_interval, port, password)

    # Register the hub.
    hass.data[DOMAIN][name] = {"hub": hub}

    for component in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, component)
        )
    return True


async def async_unload_entry(hass: HomeAssistant, entry):
    """Unload Raise3D entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(
                    entry, component)
                for component in PLATFORMS
            ]
        )
    )
    if not unload_ok:
        return False

    hass.data[DOMAIN].pop(entry.data["name"])
    return True


class Raise3dHub:
    """Thread safe wrapper class."""

    def __init__(
        self,
        hass: HomeAssistant,
        name,
        host,
        scan_interval,
        port,
        password
    ) -> None:
        """Initialize the hub."""
        self._hass = hass
        self._host = host
        self._lock = threading.Lock()
        self._name = name
        self._scan_interval = timedelta(seconds=scan_interval)
        self._port = port
        self._password = password
        self.token = None

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

    async def async_refresh_api_data(self, _now: Optional[int] = None) -> None:  # noqa: UP007
        """Time to update."""
        if not self._sensors:
            return

        try:
            update_result = await self.fetch_raise3d_data()
        except Exception as e:
            _LOGGER.debug("Exception: %s", repr(e.args))
            update_result = False

        if update_result:
            for update_callback in self._sensors:
                update_callback()

    @property
    def name(self):
        """Return the name of this hub."""
        return self._name

    async def fetch_raise3d_data(self):
        """Get data from api."""
        result = await self._hass.async_add_executor_job(fetch_data, self._host, self._port, self._password)
        self.data = result
        return True


def mergeJsonObjects(obj_1, obj_2):
    """Do merge two JSON objects from API."""
    hold_json_obj = {}
    for item_1 in obj_1:
        # We'll also loop through every item in the json_obj_2 dictionary
        for item_2 in obj_2:
            # Now let's compare whether they are the same KEYS (not values)
            if item_1 == item_2:
                # if they match, we create a list to store the array
                hold_array = {**obj_1[item_1], **obj_2[item_1]}

                # finally putting the array to our hold_json_obj
                hold_json_obj[item_1] = hold_array
            else:
                # if they don't match, check if the key already exists in the
                # hold_json_obj because we might be iterating json_obj_2 for the second time.
                if item_2 not in hold_json_obj:
                    # add the ummatched array to hold_json_obj
                    hold_json_obj[item_2] = obj_2[item_2]

    return hold_json_obj


# switch on simulation data
CONST_DEBUG = False


def fetch_data(url: str, port: int, password: str):
    """Get data."""
    JSON_data = {}
    token = None
    # _LOGGER.debug("Fetching raise3d datas with REST API")
    # _LOGGER.debug("Parameter: %s, %s, %s", url, port, password)

    printer = r3d.raise3d()

    # get new token
    token = printer.getLogin(url, str(port), password)
    if token is None:
        #_LOGGER.debug("Token not received!")

    # get info
    if token is not None:
        rc = printer.getInfo(url, str(port), token)
        if rc is not None:
            JSON_data = rc

    # get camera info
    if token is not None:
        rc = printer.getCameraInformation(url, str(port), token)
        if rc is not None:
            # merge JSON data
            JSON_data = mergeJsonObjects(JSON_data, rc)

    # get printer running status
    if token is not None:
        rc = printer.getPrinterRunningStatus(url, str(port), token)
        if rc is not None:
            # merge JSON data
            JSON_data = mergeJsonObjects(JSON_data, rc)

    # get printer getPrinterBasicInformation
    if token is not None:
        rc = printer.getPrinterBasicInformation(url, str(port), token)
        if rc is not None:
            # merge JSON data
            JSON_data = mergeJsonObjects(JSON_data, rc)

    # get printer left nozzle information
    if token is not None:
        rc = printer.getLeftNozzleInformation(url, str(port), token)
        if rc is not None:
            # merge JSON data
            JSON_data = mergeJsonObjects(JSON_data, rc)

    # get printer right nozzle information
    if token is not None:
        rc = printer.getRightNozzleInformation(url, str(port), token)
        if rc is not None:
            # merge JSON data
            JSON_data = mergeJsonObjects(JSON_data, rc)

    # get printer current job status
    if token is not None:
        rc = printer.getCurrentJob(url, str(port), token)
        if rc is not None:
            # merge JSON data
            JSON_data = mergeJsonObjects(JSON_data, rc)

    if CONST_DEBUG is True:
        # simulate recorded data from file
        JSON_data = printer.getSimulatedData()

    return JSON_data
