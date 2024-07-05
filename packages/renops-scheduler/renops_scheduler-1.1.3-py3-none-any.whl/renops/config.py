import os
import uuid
from enum import Enum


class user:
    uuid = str(uuid.uuid4())[:8]


class ipinfo:
    url = "https://ipinfo.io/json"


class geocoder:
    url = "https://nominatim.openstreetmap.org"


class renopsapi:
    # Test endpoint
    # renewable_potential = "http://127.0.0.1:8000/v1/forecast/renewable_potential"
    renewable_potential = (
        "https://renops-api-tango.xlab.si/v1/forecast/renewable_potential"
    )
    price = "https://renops-api-tango.xlab.si/v1/forecast/day_ahead_prices"
    carbon_emissions = "https://renops-api-tango.xlab.si/v1/forecast/carbon_emissions"

    key = os.getenv("RENOPSAPI_KEY")
    if key is None:
        msg = "RENOPSAPI_KEY environment variable is not set."
        msg += " Export it with your API key to remove this error."
        raise ValueError(msg)
    max_retries = 5
    secs_between_retries = 15


class runtime:
    verbose = False
    sleep_seconds = 10
    min_savings_perc = 5  # If savings too small, we execute now

    @classmethod
    def set_verbose(cls, value):
        cls.verbose = value


class OptimisationType(Enum):
    renewable_potential = "renewable_potential"
    price = "price"
    carbon_emissions = "carbon_emissions"
