import subprocess
import time
from datetime import datetime
from typing import Callable, Tuple, Union

from loguru import logger

import renops.config as conf
from renops.datafetcher import DataFetcher


def parse_time(time_string):
    return datetime.strptime(time_string, "%Y-%m-%d %H:%M:%S")


def wait_until(target_time):
    while int(time.time()) < target_time:
        time.sleep(conf.runtime.sleep_seconds)  # Sleep for a bit to not hog the CPU


def execute_script(script_path):
    subprocess.run(["python3", script_path])


def hour_to_second(hour: int) -> int:
    "Converts hours to seconds"
    return hour * 3600


def convert_seconds_to_hour(seconds: int) -> int:
    "Converts seconds to hour with no residual"
    return int(seconds // 3600)


def convert_seconds_to_minutes(seconds: int) -> int:
    "Converts seconds to minutes with no residual"
    return int((seconds % 3600) // 60)


def to_datetime(epoch):
    return datetime.fromtimestamp(epoch).strftime("%Y-%d-%m %H:%M:%S")


class Scheduler:
    """
    Scheduler to optmise scheduling of energy intensive tasks
    Args:
        deadline (int): The deadline for the scheduled task.
        runtime (int): The runtime required for the task.
        location (str): The location where the task will be executed.
        action (Callable): The function to be executed.
        optimise_type (str, optional): The type of optimization optons are "price", "carbon_emmisions",
                                       "renewable_potential". Defaults to "renewable_potential".
        optimise_price (bool, optional): Deprecated. Use 'optimise_type' instead. Defaults to False.
        verbose (bool, optional): Flag to enable verbose output. Defaults to False.
        argument (Tuple[Union[int, str], ...], optional): Arguments for the action function. Defaults to ().
        kwargs (Union[dict, None], optional): Keyword arguments for the action function. Defaults to {}.

    Raises:
        DeprecationWarning: If 'optimise_price' is used.
        ValueError: If an invalid 'optimise_type' is provided.

    Attributes:
        deadline (int): The deadline for the scheduled task.
        runtime (int): The runtime required for the task.
        location (str): The location where the task will be executed.
        v (bool): Verbose flag.
        optimise_type (str): The type of optimization.
        action (Callable): The function to be executed.
        argument (Tuple[Union[int, str], ...]): Arguments for the action function.
        kwargs (dict): Keyword arguments for the action function.
    """

    def __init__(
        self,
        deadline: int,
        runtime: int,
        location: str,
        action: Callable,
        optimise_type: str = "renewable_potential",
        optimise_price: bool = False,
        verbose: bool = False,
        argument: Tuple[Union[int, str], ...] = (),
        kwargs: Union[dict, None] = {},
    ) -> None:
        if optimise_price:
            optimise_type = "price"
            raise DeprecationWarning(
                "'optimise_price' is deprecated and will be removed in future versions. Use 'optimise_type' instead."
            )
        self.deadline = deadline
        self.runtime = runtime
        self.location = location
        self.v = verbose
        # Allow optimise_type to be a string
        # Convert string optimise_type to OptimisationType enum
        try:
            self.optimise_type = conf.OptimisationType[optimise_type]
        except KeyError:
            raise ValueError(
                f"Invalid option '{optimise_type}', must be one of {[e.value for e in conf.OptimisationType]}."
            )  # noqa

        self.optimise_type = optimise_type
        self.action = action
        self.argument = argument
        self.kwargs = kwargs if kwargs is not None else {}

    def get_data(self):
        fetcher = DataFetcher(location=self.location)
        return fetcher.fetch(self.optimise_type)

    def _preprocess_data(self, data):

        # Resample to 2H buckets
        res = data.resample("2h").agg(
            {
                "metric": "mean",
                "epoch": "first",
                "timestamps_hourly": "first",
            }
        )

        # Sort to minimise renewable potential
        res = res.set_index("epoch")

        # In case of rewewable potential we maximise, in case of price and
        # emissions we minimise
        ascending = False if self.optimise_type == "renewable_potential" else True

        res = res.sort_values(by=["metric"], ascending=ascending)

        return res

    def _extract_epochs(self):
        self.current_epoch = int(time.time())
        self.deadline_epoch = self.current_epoch + hour_to_second(self.deadline)
        self.start_execution_epoch = self.deadline_epoch - hour_to_second(self.runtime)

        return None

    def _filter_samples(self, res):
        filtered_res = res[
            (res.index >= self.current_epoch)
            & (res.index <= self.start_execution_epoch)
        ]
        filtered_res = filtered_res.loc[res.metric != 0]
        return filtered_res

    def _get_current_renewables(self, data):
        renewables_now = data[data.epoch >= self.current_epoch]
        renewables_now = renewables_now.metric.values[0].round(2)
        return renewables_now

    def _update_global_config(self):
        conf.runtime.set_verbose(self.v)

    def _calculate_estimated_improvement(self, val_now: float, val_min: float) -> float:
        """Returns estimated precent reducing given optmisation type
        The lower the better, i.e. -5 would save 5 %.

        Args:
            data (pd.DataFrame): dataframe populated with predictions
        """
        diff = val_min - val_now
        diff_perc = (diff / val_now) * 100

        if self.optimise_type in ["price", "carbon_emissions"]:
            diff_perc *= (
                -1
            )  # In case of price and carbon we minimise, in case of renewable we maxismise

        return diff_perc

    def _print_info_for_instant_execution(self):
        if self.optimise_type == "price":
            logger.info(f"Current energy price is: {self.renewables_now} EUR/MWh")
        elif self.optimise_type == "carbon_emissions":
            logger.info(
                f"Current carbon emissions are: {self.renewables_now} gCO2eq/kWh"
            )
        elif self.optimise_type == "renewable_potential":
            logger.info(f"Current renewable potential is: {self.renewables_now}")

    def run(self):
        self._update_global_config()
        data = self.get_data()
        res = self._preprocess_data(data)
        self._extract_epochs()  # extract deadilnes runtimes etc TODO
        filtered_res = self._filter_samples(res)
        self.renewables_now = self._get_current_renewables(data)
        if self.v:
            logger.info(
                f"Task has to be finished by: {to_datetime(self.deadline_epoch)}"
            )
        if len(filtered_res) <= 1:
            filtered_res[self.current_epoch] = self.renewables_now
            optimal_time = self.current_epoch

            if self.v:
                logger.info("No renewable window whitin a given deadline!")
                self._print_info_for_instant_execution()

        else:
            optimal_time = filtered_res.index[0]
            diff_seconds = optimal_time - self.current_epoch
            current_val = self._get_current_renewables(data)
            minimal_val = filtered_res.metric.values[0].round(2)
            diff_perc = self._calculate_estimated_improvement(current_val, minimal_val)

            if diff_perc < conf.runtime.min_savings_perc:
                # set optimal time to now
                optimal_time = self.current_epoch
                logger.info(
                    f"Estimated savings ({diff_perc:.2f}) % are too low, executing now!"
                )
                if self.v:
                    self._print_info_for_instant_execution()
            else:
                if self.v:
                    logger.info(
                        f"Found optimal time between {to_datetime(filtered_res.index[0])} and {to_datetime(filtered_res.index[0] + hour_to_second(self.runtime))}",  # noqa
                    )

                    if self.optimise_type == "price":
                        msg = f"Energy price at that time is: {minimal_val} EUR/MWh"

                    elif self.optimise_type == "carbon_emissions":
                        msg = f"Carbon emissions at that time are: {minimal_val} gCO2eq/kWh"

                    elif self.optimise_type == "renewable_potential":
                        msg = f"Renewable potential at that time is: {minimal_val}"

                    logger.info(
                        msg + f", where esitmated savings are {diff_perc:.2f} %"
                    )
                    logger.info(
                        f"Waiting for"
                        f" {convert_seconds_to_hour(diff_seconds)} h"
                        f" {convert_seconds_to_minutes(diff_seconds)} min"
                        f"..."
                    )

        wait_until(optimal_time)

        if self.v:
            logger.info(f"Executing action now at {datetime.now()}")
        if self.v:
            logger.info("----------------------------------------------------")
        self.action(*self.argument, **self.kwargs)
