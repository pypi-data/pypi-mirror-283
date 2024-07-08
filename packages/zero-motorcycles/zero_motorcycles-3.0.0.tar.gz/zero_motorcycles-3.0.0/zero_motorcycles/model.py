import json
from datetime import datetime


class Expire:
    def __init__(self, simexpiredate):
        self._sim_expire_date = datetime.strptime(
            f"{simexpiredate}+0000", "%Y%m%d%H%M%S%z"
        )

    @property
    def sim_expire_date(self) -> datetime:
        return self._sim_expire_date


class Unit:
    def __init__(self, unitnumber, name, active, **kwargs):
        self._unit = unitnumber
        self._name = name
        self._active = int(active) == 1

    @property
    def unit(self) -> str:
        return self._unit

    @property
    def name(self) -> str:
        return self._name

    @property
    def active(self) -> bool:
        return self._active


class Zero:
    """Zero motorcycle Object"""

    def __init__(
        self,
        unitnumber,
        name,
        mileage,
        software_version,
        longitude,
        latitude,
        altitude,
        gps_valid,
        gps_connected,
        satellites,
        velocity,
        heading,
        main_voltage,
        datetime_utc,
        address,
        soc,
        tipover,
        charging,
        chargecomplete,
        pluggedin,
        chargingtimeleft,
        storage,
        **kwargs,
    ):
        """Initialize"""
        self._unit = unitnumber
        self._vin = name
        self._mileage = float(mileage)
        self._software_version = software_version
        self._longitude = float(longitude)
        self._latitude = float(latitude)
        self._elevation = int(altitude)
        self._gps_valid = int(gps_valid) == 1
        self._gps_connected = int(gps_connected) == 1
        self._satellites = int(satellites)
        self._velocity = int(velocity)
        self._heading = int(heading)
        self._main_voltage = float(main_voltage)
        self._datetime_utc = datetime.strptime(f"{datetime_utc}+0000", "%Y%m%d%H%M%S%z")
        self._address = address
        self._soc = int(soc)
        self._tip_over = int(tipover) == 1
        self._charging = int(charging) == 1
        self._charge_complete = int(chargecomplete) == 1
        self._plugged = int(pluggedin) == 1
        self._charging_time_left = int(chargingtimeleft)
        self._storage = int(storage) == 1

    @property
    def unit(self) -> str:
        return self._unit

    @property
    def vin(self) -> str:
        return self._vin

    @property
    def mileage(self) -> float:
        return self._mileage

    @property
    def software_version(self) -> str:
        return self._software_version

    @property
    def longitude(self) -> float:
        return self._longitude

    @property
    def latitude(self) -> float:
        return self._latitude

    @property
    def elevation(self) -> int:
        return self._elevation

    @property
    def gps_valid(self) -> bool:
        return self._gps_valid

    @property
    def gps_connected(self) -> bool:
        return self._gps_connected

    @property
    def satellites(self) -> int:
        return self._satellites

    @property
    def velocity(self) -> int:
        return self._velocity

    @property
    def heading(self) -> int:
        return self._heading

    @property
    def main_voltage(self) -> float:
        return self._main_voltage

    @property
    def datetime_utc(self) -> datetime:
        return self._datetime_utc

    @property
    def address(self) -> str:
        return self._address

    @property
    def soc(self) -> int:
        return self._soc

    @property
    def tip_over(self) -> bool:
        return self._tip_over

    @property
    def charging(self) -> bool:
        return self._charging

    @property
    def charge_complete(self) -> bool:
        return self._charge_complete

    @property
    def plugged(self) -> bool:
        return self._plugged

    @property
    def charging_time_left(self) -> int:
        return self._charging_time_left

    @property
    def storage(self) -> bool:
        return self._storage

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
