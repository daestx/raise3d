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
        None
    ],

    "api_version": [
        "API version",
        "api_version",
        None,
        None
    ],

    "battery": [
        "Battery voltage",
        "battery",
        None,
        None
    ],

    "brightness": [
        "Screen brightness",
        "brightness",
        None,
        None
    ],

    "date_time": [
        "UTC Time",
        "date_time",
        None,
        None
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
        None
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
        None
    ],
    "storage_available": [
        "Availabe storage",
        "storage_available",
        None,
        None
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
        None
    ]
}

CAMERA_INFORMATION = {
    "camerserver_URI": [
        "Camera server URI",
        "camerserver_URI",
        None,
        None
    ],

    "is_camera_connected": [
        "Camera status",
        "is_camera_connected",
        None,
        None
    ],

    "password": [
        "Password",
        "password",
        None,
        None
    ],

    "user_name": [
        "User",
        "user_name",
        None,
        None
    ]
}

PRINTER_RUNNING_STATUS = {
    "running_status": [
        "Running status",
        "running_status",
        None,
        None
    ]
}

PRINTER_BASIC_INFORMATION = {
    "fan_cur_speed": [
        "Current fan speed",
        "fan_cur_speed",
        None,
        None
    ],

    "fan_tar_speed": [
        "Target fan speed",
        "fan_tar_speed",
        None,
        None
    ],

    "feed_cur_rate": [
        "Current nozzle feed speed",
        "feed_cur_rate",
        None,
        None
    ],

    "feed_tar_rate": [
        "Target nozzle feed speed",
        "feed_tar_rate",
        None,
        None
    ],

    "heatbed_cur_temp": [
        "Current heatbed temp",
        "heatbed_cur_temp",
        None,
        None
    ],

    "heatbed_tar_temp": [
        "Target heatbed temp",
        "heatbed_tar_temp",
        None,
        None
    ]
}

PRINTER_NOZZLE_INFORMATION = {
    "LN_flow_cur_rate": [
        "Left nozzle current extrusion speed",
        "LN_flow_cur_rate",
        None,
        None
    ],

    "LN_flow_tar_rate": [
        "Left nozzle target extrusion speed",
        "LN_flow_tar_rate",
        None,
        None
    ],

    "LN_nozzle_cur_temp": [
        "Left nozzle current temperature",
        "LN_nozzle_cur_temp",
        None,
        None
    ],

    "LN_nozzle_tar_temp": [
        "Left nozzle target temperature",
        "LN_nozzle_tar_temp",
        None,
        None
    ],

    "RN_flow_cur_rate": [
        "Right nozzle current extrusion speed",
        "RN_flow_cur_rate",
        None,
        None
    ],

    "RN_flow_tar_rate": [
        "Right nozzle target extrusion speed",
        "RN_flow_tar_rate",
        None,
        None
    ],

    "RN_nozzle_cur_temp": [
        "Right nozzle current temperature",
        "RN_nozzle_cur_temp",
        None,
        None
    ],

    "RN_nozzle_tar_temp": [
        "Right nozzle target temperature",
        "RN_nozzle_tar_temp",
        None,
        None
    ]
}

PRINTER_CURRENT_JOB_INFORMATION = {
    "file_name": [
        "File name",
        "file_name",
        None,
        None
    ],

    "print_progress": [
        "Print progress",
        "print_progress",
        None,
        None
    ],

    "printed_layer": [
        "Printerd layers",
        "printed_layer",
        None,
        None
    ],

    "total_layer": [
        "Total layers",
        "total_layer",
        None,
        None
    ],

    "printed_time": [
        "Printing time",
        "printed_time",
        None,
        None
    ],

    "total_time": [
        "Total time",
        "total_time",
        None,
        None
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
        None
    ]
}

