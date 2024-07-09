from datetime import datetime
from enum import IntEnum
from typing import Any


class ProbeBatteryLevel(IntEnum):
    """Map battery status to corresponding level in percentage.

    The calculated percentage is only an approximation.
    """

    NORMAL = 100
    FAIR = 50
    POOR = 10


class Sensor:
    type: str | None = None
    depth: int | None = None
    value: float | None = None
    unit: str | None = None
    timestamp: datetime | None = None
    soil: str | None = None

    def __init__(self, id: str):
        self.id = id

    def __repr__(self) -> str:
        return self.id

    def __str__(self) -> str:
        parts = [
            str(self.timestamp),
            f"{self.type:14}",
            f"{self.value:2.0f} {self.unit:2}",
        ]
        if self.depth is not None:
            parts.append(f"@ {self.depth} cm")
        if self.soil is not None:
            parts.append(f"in {self.soil}")
        return " ".join(parts)

    def update(self, reading: dict[str, Any], soil: str | None = None) -> None:
        self.type = reading["type"]
        self.depth = int(reading["depth"]) if "depth" in reading else None
        self.value = float(reading["value"])
        self.unit = reading["unit"]
        if reading["timestamp"] is not None:
            self.timestamp = datetime.fromisoformat(reading["timestamp"])
        self.soil = soil


class Probe:
    name: str | None = None
    sku: str | None = None
    state: str | None = None
    location_id: int | None = None
    location: str | None = None
    latitude: float | None = None
    longitude: float | None = None

    def __init__(self, serial: str):
        self.serial = serial
        self.__sensors: dict[str, Sensor] = {}

    def __find_soil(
        self,
        soils: dict[str, str],
        profile: list[dict[str, Any]],
        reading: dict[str, Any],
    ) -> str | None:
        """Find the soil at depth based on the soil profile

        We can safely assume profile is sorted on depth.
        """
        soil = None
        if reading["type"] == "MOISTURE" and "depth" in reading:
            for layer in profile:
                if layer["depth"] > reading["depth"]:
                    break
                soil = soils.get(layer["soil"])
        return soil

    def __update_sensor(
        self, id: str, reading: dict[str, Any], soil: str | None = None
    ) -> None:
        if id not in self.__sensors:
            self.__sensors[id] = Sensor(id)
        self.__sensors[id].update(reading, soil)

    def update(
        self, soils: dict[str, str], locations: dict[int, str], probe: dict[str, Any]
    ) -> None:
        self.id = probe["id"]
        self.name = probe["name"]
        self.sku = probe["sku"]
        self.state = probe["state"]

        self.latitude = probe.get("latitude")
        self.longitude = probe.get("longitude")

        if "location_id" in probe:
            self.location_id = int(probe["location_id"])
            self.location = locations.get(self.location_id)
        else:
            self.location_id = None
            self.location = None

        timestamp = probe["status"].get("last_update")
        if timestamp is not None:
            self.timestamp = datetime.fromisoformat(timestamp)

        if "last_readings" in probe["status"]:
            for reading in probe["status"]["last_readings"]:
                id = f"{probe['serial']}-{reading['type']}"
                if "depth" in reading and reading["depth"] > 0:
                    id += "-" + str(reading["depth"])
                soil = self.__find_soil(soils, probe["soil_profile"], reading)
                self.__update_sensor(id, reading, soil)

        if "battery" in probe["status"]:
            self.__update_sensor(
                f"{probe['serial']}-BATTERY",
                {
                    "type": "BATTERY",
                    "value": ProbeBatteryLevel[probe["status"].get("battery")].value,
                    "unit": "%",
                    "timestamp": timestamp,
                },
            )

        if "rssi" in probe["status"]:
            self.__update_sensor(
                f"{probe['serial']}-RSSI",
                {
                    "type": "RSSI",
                    "value": probe["status"]["rssi"],
                    "unit": "dBm",
                    "timestamp": timestamp,
                },
            )

    def sensors(self) -> list[Sensor]:
        """Get the list of sensors of a probe"""
        return list(self.__sensors.values())

    def __str__(self) -> str:
        parts = [f"-{self.serial}-"]
        if self.name != self.serial:
            parts.append(f"({self.name})")
        if self.location is not None:
            parts.append(f"@{self.location}")
        return " ".join(parts)

    def __repr__(self) -> str:
        return f"{self.serial}"
