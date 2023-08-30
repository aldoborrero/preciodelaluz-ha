from pytest_mock import MockerFixture

from custom_components.preciodelaluz.api import PrecioDeLaLuzAPI


def test_get_all_prices(mocker: MockerFixture):
    mock_response = mocker.patch("requests.get")
    mock_response().json.return_value = {"data": "test_data"}

    api = PrecioDeLaLuzAPI()
    result = api.get_all_prices()

    assert result == {"data": "test_data"}
    mock_response.assert_called_with(
        "https://api.preciodelaluz.org/v1/prices/all?zone=PCB", params=None, timeout=10
    )


def test_get_avg_price(mocker: MockerFixture):
    mock_response = mocker.patch("requests.get")
    mock_response().json.return_value = {"average": "test_avg"}

    api = PrecioDeLaLuzAPI()
    result = api.get_avg_price()

    assert result == {"average": "test_avg"}
    mock_response.assert_called_with(
        "https://api.preciodelaluz.org/v1/prices/avg?zone=PCB", params=None, timeout=10
    )
