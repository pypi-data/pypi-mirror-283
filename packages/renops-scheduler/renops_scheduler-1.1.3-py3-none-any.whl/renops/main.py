#!/usr/bin/env python3

import argparse
import sys
import warnings
from argparse import RawTextHelpFormatter

from loguru import logger

from renops.config import OptimisationType
from renops.geoshifter import GeoShift
from renops.scheduler import Scheduler, execute_script
from renops.utils import read_json_from_filename

warnings.simplefilter("always", DeprecationWarning)


def main():
    try:
        run()

    except ValueError as error:
        logger.error(f"ValueError: {error}")
        sys.exit(1)  # Exiting with status code 1 signifies an error

    except KeyboardInterrupt:
        logger.error("\nKeyboard interrupt detected. Exiting.")
        sys.exit(0)  # Exiting with status code 0 signifies a clean exit

    except Exception as ex:
        logger.error(f"An unexpected error occurred: {ex}")
        sys.exit(1)  # Exiting with status code 1 for error


def run():
    logger.info("RUNNING RENOPS SCHEDULER...")
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        "script_path",
        help="Path to the script to be executed or JSON file in case of geo shifting.",
    )
    parser.add_argument(
        "-l",
        "--location",
        default=None,
        help=(
            "Location can be specified in two ways:\n\n"
            '1. Pass a specific location as a string, e.g., "Berlin, Germany".\n\n'
            "2. Use automatic location detection based on IP address.\n"
            " By using this tag, you agree that your IP can be used to detect your location.\n"
            "You can use any of the following values for this purpose:\n"
            "   -l a (-la)\n"
            "   -l auto\n"
            "   -l automatic\n"
        ),
    )

    parser.add_argument(
        "-gs",
        "--geo-shift",
        action="store_true",
        help="JSON on given path should be formated as:\n"
        "{\n"
        '  "hpc1": {\n'
        '    "location": "Berlin, Germany",\n'
        '    "cmd": "ssh user@hpc1 python3 train.py"\n'
        "  },\n"
        '  "hpc2": {\n'
        '    "location": "Madrid, Spain",\n'
        '    "cmd": "ssh user@hpc2 python3 train.py"\n'
        "  },\n"
        '  "hpc3": {\n'
        '    "location": "Copenhagen, Denmark",\n'
        '    "cmd": "ssh user@hpc3 python3 train.py"\n'
        "  }\n"
        "}",
    )

    parser.add_argument(
        "-r",
        "--runtime",
        type=int,
        default=None,
        help="Runtime in hours. (Not for geo shift mode)",
    )

    parser.add_argument(
        "-d",
        "--deadline",
        type=int,
        default=120,
        help="Deadline in hours, by when should script finish running (Not for geo shift mode)",  # noqa
    )

    parser.add_argument(
        "-o",
        "--optimise",
        choices=["renewable", "price", "emissions"],
        required=False,
        help=(
            "Choose an optimisation type:\n"
            " - 'renewable' (renewable potential - renewable energy availability on a scale from 0 to 1)\n"
            " - 'price' (day-ahead energy price)\n"
            " - 'emissions' (Carbon emissions in gCO2eq/kWh)\n"
        ),
    )
    parser.add_argument(
        "-op", "--optimise-price", action="store_true", help=argparse.SUPPRESS
    )

    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose mode.")

    args = parser.parse_args()

    # Check for the deprecated argument and warn the user
    if args.optimise_price:
        warnings.warn(
            "'--optimise-price' is deprecated and will be removed in future versions. "
            "Use '--optimise price' instead.",
            DeprecationWarning,
        )
        # Map the deprecated argument to the new one if necessary
        args.optimise = "price"

    if args.optimise is None:
        warnings.warn(
            "Default optimisation type is deprecated and will be mandatory in future versions. "
            "Setting optimise flag to 'renewable'. "
            "Use '--optimise ' instead.",
            DeprecationWarning,
        )
        args.optimise = "renewable"

    optimisation_map = {
        "renewable": OptimisationType.renewable_potential,
        "price": OptimisationType.price,
        "emissions": OptimisationType.carbon_emissions,
    }

    optimise_type = optimisation_map[args.optimise].value

    if args.geo_shift:
        logger.info("Geo shift mode specified, shifting in space...")
        if not args.script_path.endswith(".json"):
            raise ValueError("The input file must be a JSON file.")
        s = GeoShift(
            locations=read_json_from_filename(args.script_path),
            optimise_type=optimise_type,
            verbose=args.verbose,
        )
        s.shift()

    elif args.location:
        logger.info("Location specified, shifting in time...")
        args = parser.parse_args()
        if not args.runtime:
            logger.info("Runtime not specified, using default setting of 3 hours!")
            args.runtime = 3

        s = Scheduler(
            deadline=args.deadline,
            runtime=args.runtime,
            location=args.location,
            optimise_type=optimise_type,
            verbose=args.verbose,
            action=execute_script,
            argument=([args.script_path]),
        )
        s.run()

    else:
        raise ValueError(
            "Specifiy either location (-l) or geo shift mode (-gs). Check --help for more details."
        )  # noqa


if __name__ == "__main__":
    main()
