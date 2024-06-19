"""Constants for Raise3D printer configuration."""
from logging import Logger, getLogger

""" from homeassistant.const import (
    UnitOfTime,
    PERCENTAGE,
    UnitOfTemperature,
    UnitOfMass,
    UnitOfPower,
    UnitOfEnergy,
)
 """

LOGGER: Logger = getLogger(__package__)

NAME = "Raise3D"
DOMAIN = "raise3d"
VERSION = "0.0.0"
ATTRIBUTION = "Data provided by http://jsonplaceholder.typicode.com/"

DEFAULT_NAME = "Raise3D"
DEFAULT_SCAN_INTERVAL = 30
DEFAULT_PORT = 10800
DEFAULT_IP = "192.168.110.25"
DEFAULT_PASSWORD = "password"

# titles in configuration flows are define in strings and translation json files
CONF_PORT = "conf_port"
CONF_PASSWORD = "conf_password"

ATTR_MANUFACTURER = "Raise 3D"
ATTR_MODEL = "Pro2"


#Printer System Information
PRINTER_SYSTEM_INFORMATION = {
    "serial_number": [
        "Serial number",
        "Serial_number",
        None,
        "mdi:numeric"
    ],

    "api_version": [
        "API version",
        "api_version",
        None,
        "mdi:numeric"
    ],

    "battery": [
        "Battery voltage",
        "battery",
        None,
        "mdi:battery-outline"
    ],

    "brightness": [
        "Screen brightness",
        "brightness",
        None,
        "mdi:brightness-6"
    ],

    "date_time": [
        "UTC Time",
        "date_time",
        None,
        "mdi:calendar-clock"
    ],

    "firmware_version": [
        "Firmware version",
        "firmware_version",
        None,
        None
    ],

    "language": [
        "Language locales",
        "language",
        None,
        None
    ],

    "machine_id": [
        "Printer ID",
        "machine_id",
        None,
        "mdi:printer-3d"
    ],

    "machine_ip": [
        "Printer IP",
        "machine_ip",
        None,
        None
    ],

    "machine_name": [
        "Printer name",
        "machine_name",
        None,
        None
    ],

    "model": [
        "Model",
        "model",
        None,
        None
    ],
    "nozzies_num": [
        "Number of nozzles",
        "nozzies_num",
        None,
        "mdi:printer-3d-nozzle"
    ],
    "storage_available": [
        "Availabe storage",
        "storage_available",
        None,
        "mdi:sd"
    ],

    "update": [
        "Update",
        "update",
        None,
        None
    ],

    "version": [
        "Version",
        "version",
        None,
        "mdi:numeric"
    ]
}

CAMERA_INFORMATION = {
    "camerserver_URI": [
        "Camera server URI",
        "camerserver_URI",
        None,
        "mdi:ip-network-outline"
    ],

    "is_camera_connected": [
        "Camera status",
        "is_camera_connected",
        None,
        "mdi:webcam"
    ],

    "password": [
        "Password",
        "password",
        None,
        "mdi:key"
    ],

    "user_name": [
        "User",
        "user_name",
        None,
        "mdi:account"
    ]
}

PRINTER_RUNNING_STATUS = {
    "running_status": [
        "Running status",
        "running_status",
        None,
        "mdi:state-machine"
    ]
}

PRINTER_BASIC_INFORMATION = {
    "fan_cur_speed": [
        "Current fan speed",
        "fan_cur_speed",
        None,
        "mdi:fan"
    ],

    "fan_tar_speed": [
        "Target fan speed",
        "fan_tar_speed",
        None,
        "mdi:fan"
    ],

    "feed_cur_rate": [
        "Current nozzle feed speed",
        "feed_cur_rate",
        None,
        "mdi:printer-3d-nozzle-outline"
    ],

    "feed_tar_rate": [
        "Target nozzle feed speed",
        "feed_tar_rate",
        None,
        "mdi:printer-3d-nozzle-outline"
    ],

    "heatbed_cur_temp": [
        "Current heatbed temp",
        "heatbed_cur_temp",
        None,
        "mdi:heat-wave"
    ],

    "heatbed_tar_temp": [
        "Target heatbed temp",
        "heatbed_tar_temp",
        None,
        "mdi:heat-wave"
    ]
}

PRINTER_NOZZLE_INFORMATION = {
    "LN_flow_cur_rate": [
        "Left nozzle current extrusion speed",
        "LN_flow_cur_rate",
        None,
        "mdi:printer-3d-nozzle-outline"
    ],

    "LN_flow_tar_rate": [
        "Left nozzle target extrusion speed",
        "LN_flow_tar_rate",
        None,
        "mdi:printer-3d-nozzle-outline"
    ],

    "LN_nozzle_cur_temp": [
        "Left nozzle current temperature",
        "LN_nozzle_cur_temp",
        None,
        "mdi:printer-3d-nozzle-heat"
    ],

    "LN_nozzle_tar_temp": [
        "Left nozzle target temperature",
        "LN_nozzle_tar_temp",
        None,
        "mdi:printer-3d-nozzle-heat"
    ],

    "RN_flow_cur_rate": [
        "Right nozzle current extrusion speed",
        "RN_flow_cur_rate",
        None,
        "mdi:printer-3d-nozzle-outline"
    ],

    "RN_flow_tar_rate": [
        "Right nozzle target extrusion speed",
        "RN_flow_tar_rate",
        None,
        "mdi:printer-3d-nozzle-outline"
    ],

    "RN_nozzle_cur_temp": [
        "Right nozzle current temperature",
        "RN_nozzle_cur_temp",
        None,
        "mdi:printer-3d-nozzle-heat"
    ],

    "RN_nozzle_tar_temp": [
        "Right nozzle target temperature",
        "RN_nozzle_tar_temp",
        None,
        "mdi:printer-3d-nozzle-heat"
    ]
}

PRINTER_CURRENT_JOB_INFORMATION = {
    "file_name": [
        "File name",
        "file_name",
        None,
        "mdi:file-outline"
    ],

    "print_progress": [
        "Print progress",
        "print_progress",
        None,
        "mdi:progress-helper"
    ],

    "printed_layer": [
        "Printerd layers",
        "printed_layer",
        None,
        "mdi:layers"
    ],

    "total_layer": [
        "Total layers",
        "total_layer",
        None,
        "mdi:layers"
    ],

    "printed_time": [
        "Printing time",
        "printed_time",
        None,
        "mdi:clock"
    ],

    "total_time": [
        "Total time",
        "total_time",
        None,
        "mdi:clock"
    ],

    "remaining_time": [
        "Remaining time",
        "remaining_time",
        None,
        "mdi:clock"
    ],


    "job_id": [
        "Job ID",
        "job_id",
        None,
        None
    ],

    "job_status": [
        "Job status",
        "job_status",
        None,
        "mdi:bell-circle-outline"
    ]
}

