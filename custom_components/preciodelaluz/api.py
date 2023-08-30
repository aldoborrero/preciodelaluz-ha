import requests

BASE_URL = "https://api.preciodelaluz.org"


class PrecioDeLaLuzAPI:
    def __init__(self, zone="PCB", convert_units=False):
        self.zone = zone
        self.convert_units = convert_units

    def _make_request(self, endpoint, params=None):
        url = f"{BASE_URL}/{endpoint}"
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            # Convert the units if required
            if self.convert_units:
                data = self._convert_units(data)
            return data

        except requests.RequestException as ex:
            raise Exception(f"Error fetching data from PrecioDelaluz API: {ex}")

    def _convert_units(self, data):
        """Convert price from €/MWh to €/kWh"""
        if isinstance(data, list):  # If the result is a list of price data
            return [self._convert_single_entry(item) for item in data]
        else:
            return self._convert_single_entry(data)

    @staticmethod
    def _convert_single_entry(entry):
        if entry.get("units") == "€/MWh":
            entry["price"] /= 1000  # Convert MWh to kWh
            entry["units"] = "€/kWh"
        return entry

    def get_all_prices(self):
        return self._make_request(f"v1/prices/all?zone={self.zone}")

    def get_avg_price(self):
        return self._make_request(f"v1/prices/avg?zone={self.zone}")

    def get_max_price(self):
        return self._make_request(f"v1/prices/max?zone={self.zone}")

    def get_min_price(self):
        return self._make_request(f"v1/prices/min?zone={self.zone}")

    def get_current_price(self):
        return self._make_request(f"v1/prices/now?zone={self.zone}")

    def get_cheapest_prices(self, n=2):
        return self._make_request(
            f"v1/prices/cheapests?zone={self.zone}", params={"n": n}
        )
