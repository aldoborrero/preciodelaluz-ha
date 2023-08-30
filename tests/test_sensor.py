from unittest.mock import MagicMock, patch

from homeassistant.const import CONF_NAME
import pytest

from custom_components.preciodelaluz.sensor import (
    PrecioDelaluzSensor,
    async_setup_platform,
)


def test_sensor_name():
    coordinator_mock = MagicMock()
    api_mock = MagicMock()
    sensor = PrecioDelaluzSensor(
        coordinator_mock, api_mock, "TestName", "TestType", "all"
    )

    assert sensor.name == "TestName TestType"


def test_sensor_update():
    coordinator_mock = MagicMock()
    coordinator_mock.data = {"all": "test_value"}
    api_mock = MagicMock()

    sensor = PrecioDelaluzSensor(
        coordinator_mock, api_mock, "TestName", "TestType", "all"
    )
    sensor.update()

    assert sensor.state == "test_value"


def test_sensor_update_with_api_error():
    coordinator_mock = MagicMock()
    coordinator_mock.data = None
    api_mock = MagicMock()

    sensor = PrecioDelaluzSensor(
        coordinator_mock, api_mock, "TestName", "TestType", "all"
    )
    sensor.update()

    assert sensor.state is None


def test_sensor_update_max_price():
    coordinator_mock = MagicMock()
    coordinator_mock.data = {"max": 150}
    api_mock = MagicMock()

    sensor = PrecioDelaluzSensor(
        coordinator_mock, api_mock, "TestName", "Max Price", "max"
    )
    sensor.update()

    assert sensor.state == 150


def test_sensor_update_current_price():
    coordinator_mock = MagicMock()
    coordinator_mock.data = {"all": {10: 100}}
    api_mock = MagicMock()

    with patch("custom_components.preciodelaluz.sensor.datetime") as mock_datetime:
        mock_datetime.now.return_value.hour = 10

        sensor = PrecioDelaluzSensor(
            coordinator_mock, api_mock, "TestName", "Current Price", "now"
        )
        sensor.update()

    assert sensor.state == 100


@pytest.mark.asyncio
async def test_setup_platform(mocker):
    api_mock = mocker.MagicMock()
    # Mock the PrecioDelaluzAPI class to return our mock object
    mocker.patch(
        "custom_components.preciodelaluz.sensor.PrecioDeLaLuzAPI", return_value=api_mock
    )

    add_entities_mock = mocker.MagicMock()

    await async_setup_platform(None, {CONF_NAME: "TestName"}, add_entities_mock)

    add_entities_mock.assert_called_once()
