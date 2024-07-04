import datetime
from unittest.mock import Mock

import pytest
from voluptuous import (
    All,
    Any,
    Coerce,
    Range,
    Schema,
)

from kasa import Device, EmeterStatus, Module
from kasa.interfaces.energy import Energy
from kasa.iot import IotDevice, IotStrip
from kasa.iot.modules.emeter import Emeter

from .conftest import has_emeter, has_emeter_iot, no_emeter

CURRENT_CONSUMPTION_SCHEMA = Schema(
    Any(
        {
            "voltage": Any(All(float, Range(min=0, max=300)), None),
            "power": Any(Coerce(float), None),
            "total": Any(Coerce(float), None),
            "current": Any(All(float), None),
            "voltage_mv": Any(All(float, Range(min=0, max=300000)), int, None),
            "power_mw": Any(Coerce(float), None),
            "total_wh": Any(Coerce(float), None),
            "current_ma": Any(All(float), int, None),
            "slot_id": Any(Coerce(int), None),
        },
        None,
    )
)


@no_emeter
async def test_no_emeter(dev):
    assert not dev.has_emeter

    with pytest.raises(AttributeError):
        await dev.get_emeter_realtime()
    # Only iot devices support the historical stats so other
    # devices will not implement the methods below
    if isinstance(dev, IotDevice):
        with pytest.raises(AttributeError):
            await dev.get_emeter_daily()
        with pytest.raises(AttributeError):
            await dev.get_emeter_monthly()
        with pytest.raises(AttributeError):
            await dev.erase_emeter_stats()


@has_emeter
async def test_get_emeter_realtime(dev):
    assert dev.has_emeter

    current_emeter = await dev.get_emeter_realtime()
    CURRENT_CONSUMPTION_SCHEMA(current_emeter)


@has_emeter_iot
@pytest.mark.requires_dummy
async def test_get_emeter_daily(dev):
    assert dev.has_emeter

    assert await dev.get_emeter_daily(year=1900, month=1) == {}

    d = await dev.get_emeter_daily()
    assert len(d) > 0

    k, v = d.popitem()
    assert isinstance(k, int)
    assert isinstance(v, float)

    # Test kwh (energy, energy_wh)
    d = await dev.get_emeter_daily(kwh=False)
    k2, v2 = d.popitem()
    assert v * 1000 == v2


@has_emeter_iot
@pytest.mark.requires_dummy
async def test_get_emeter_monthly(dev):
    assert dev.has_emeter

    assert await dev.get_emeter_monthly(year=1900) == {}

    d = await dev.get_emeter_monthly()
    assert len(d) > 0

    k, v = d.popitem()
    assert isinstance(k, int)
    assert isinstance(v, float)

    # Test kwh (energy, energy_wh)
    d = await dev.get_emeter_monthly(kwh=False)
    k2, v2 = d.popitem()
    assert v * 1000 == v2


@has_emeter_iot
async def test_emeter_status(dev):
    assert dev.has_emeter

    d = await dev.get_emeter_realtime()

    with pytest.raises(KeyError):
        assert d["foo"]

    assert d["power_mw"] == d["power"] * 1000
    # bulbs have only power according to tplink simulator.
    if not dev.is_bulb and not dev.is_light_strip:
        assert d["voltage_mv"] == d["voltage"] * 1000

        assert d["current_ma"] == d["current"] * 1000
        assert d["total_wh"] == d["total"] * 1000


@pytest.mark.skip("not clearing your stats..")
@has_emeter
async def test_erase_emeter_stats(dev):
    assert dev.has_emeter

    await dev.erase_emeter()


@has_emeter_iot
async def test_current_consumption(dev):
    if dev.has_emeter:
        x = dev.current_consumption
        assert isinstance(x, float)
        assert x >= 0.0
    else:
        assert dev.current_consumption is None


async def test_emeterstatus_missing_current():
    """KL125 does not report 'current' for emeter."""
    regular = EmeterStatus(
        {"err_code": 0, "power_mw": 0, "total_wh": 13, "current_ma": 123}
    )
    assert regular["current"] == 0.123

    with pytest.raises(KeyError):
        regular["invalid_key"]

    missing_current = EmeterStatus({"err_code": 0, "power_mw": 0, "total_wh": 13})
    assert missing_current["current"] is None


async def test_emeter_daily():
    """Test fetching the emeter for today.

    This test uses inline data since the fixtures
    will not have data for the current day.
    """
    emeter_data = {
        "get_daystat": {
            "day_list": [{"day": 1, "energy_wh": 8, "month": 1, "year": 2023}],
            "err_code": 0,
        }
    }

    class MockEmeter(Emeter):
        @property
        def data(self):
            return emeter_data

    emeter = MockEmeter(Mock(), "emeter")
    now = datetime.datetime.now()
    emeter_data["get_daystat"]["day_list"].append(
        {"day": now.day, "energy_wh": 500, "month": now.month, "year": now.year}
    )
    assert emeter.emeter_today == 0.500


@has_emeter
async def test_supported(dev: Device):
    energy_module = dev.modules.get(Module.Energy)
    assert energy_module
    if isinstance(dev, IotDevice):
        info = (
            dev._last_update
            if not isinstance(dev, IotStrip)
            else dev.children[0].internal_state
        )
        emeter = info[energy_module._module]["get_realtime"]
        has_total = "total" in emeter or "total_wh" in emeter
        has_voltage_current = "voltage" in emeter or "voltage_mv" in emeter
        assert (
            energy_module.supports(Energy.ModuleFeature.CONSUMPTION_TOTAL) is has_total
        )
        assert (
            energy_module.supports(Energy.ModuleFeature.VOLTAGE_CURRENT)
            is has_voltage_current
        )
        assert energy_module.supports(Energy.ModuleFeature.PERIODIC_STATS) is True
    else:
        assert energy_module.supports(Energy.ModuleFeature.CONSUMPTION_TOTAL) is False
        assert energy_module.supports(Energy.ModuleFeature.VOLTAGE_CURRENT) is False
        assert energy_module.supports(Energy.ModuleFeature.PERIODIC_STATS) is False
