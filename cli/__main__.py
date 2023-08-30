import argparse
import json

from custom_components.preciodelaluz.api import PrecioDeLaLuzAPI


def main():
    parser = argparse.ArgumentParser(
        description="CLI for accessing data from PrecioDeLaLuzAPI"
    )

    parser.add_argument(
        "--type",
        choices=["all", "avg", "max", "min", "now", "cheapest"],
        required=True,
        help="""Type of data to fetch:
                all - Retrieve all prices
                avg - Get the average price
                max - Get the maximum price
                min - Get the minimum price
                now - Get the current price
                cheapest - Get the cheapest prices""",
    )

    parser.add_argument(
        "--zone", default="PCB", help="Specify the zone for the data. Default is 'PCB'."
    )

    parser.add_argument(
        "--n",
        type=int,
        default=2,
        help="""Number of cheapest prices to retrieve. 
                Only relevant if --type is set to 'cheapest'. 
                Default is 2.""",
    )

    parser.add_argument(
        "--convert-units",
        action="store_true",
        help="""Convert price units from €/MWh to €/kWh. 
                Default is not to convert.""",
    )

    args = parser.parse_args()

    api = PrecioDeLaLuzAPI(zone=args.zone, convert_units=args.convert_units)

    # Mapping CLI commands to API methods
    command_map = {
        "all": api.get_all_prices,
        "avg": api.get_avg_price,
        "max": api.get_max_price,
        "min": api.get_min_price,
        "now": api.get_current_price,
        "cheapest": lambda: api.get_cheapest_prices(n=args.n),
    }

    try:
        result = command_map[args.type]()
        print(json.dumps(result, indent=4))
    except Exception as e:
        print(f"Error occurred: {e}")


if __name__ == "__main__":
    main()
