import time

from loguru import logger

import renops.config as conf
from renops.datafetcher import DataFetcher
from renops.utils import execute_linux_command, get_closest_metric


class GeoShift:
    def __init__(
        self,
        locations: dict,
        optimise_type: str = "renewable_potential",
        verbose: bool = False,
    ):
        self.locations = locations
        self.verbose = verbose
        try:
            self.optimise_type = conf.OptimisationType[optimise_type]
        except KeyError:
            raise ValueError(
                f"Invalid option '{optimise_type}', must be one of {[e.value for e in conf.OptimisationType]}."
            )  # noqa

        self.optimise_type = optimise_type

    def check_subkeys(self, dictionary: dict) -> bool:
        for key, value in dictionary.items():
            if "location" not in value or "cmd" not in value:
                return False
        return True

    def shift(self):
        if not self.check_subkeys(self.locations):
            raise ValueError(
                'Each dictionary in the input dictionary must have a "location" and "cmd" key.'
            )

        metrics = {}
        for key, value in self.locations.items():
            current_epoch = int(time.time())
            forecast = DataFetcher(value["location"]).fetch(
                optimise_type=self.optimise_type
            )
            current_metric = get_closest_metric(forecast, current_epoch)
            if self.verbose:
                logger.info(
                    f"Current metric for {key} in {value['location']} is: {current_metric:.2f}"
                )
            metrics[key] = current_metric

        if self.optimise_type == "renewable_potential":
            best_location = max(metrics, key=metrics.get)
        else:
            best_location = min(metrics, key=metrics.get)

        ep = self.locations[best_location]

        logger.info(f'Found optimal location: {best_location}, {ep["location"]}!')
        logger.info(f"... Running specified command: {ep['cmd']}!")

        stdout, stderr = execute_linux_command(ep["cmd"])
        logger.info(f"stdout: {stdout}")
        logger.info(f"stderr: {stderr}")

        return stdout, stderr
