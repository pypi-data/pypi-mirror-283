import json
from abc import ABC, abstractmethod
import inspect
from threading import Thread
from datetime import time
from time import sleep
from typing import Optional
import os
from multiprocessing import Manager
import numpy as np
import boto3
from SmartApi.smartExceptions import DataException
from volstreet.config import logger
from volstreet.utils.communication import notifier
from volstreet.utils.core import current_time, time_to_expiry
from volstreet.utils.change_config import (
    set_notifier_level,
    set_error_notification_settings,
)
from volstreet import config
from volstreet.angel_interface.login import login, wait_for_login
from volstreet.angel_interface.interface import (
    LiveFeeds,
    fetch_book,
    lookup_and_return,
    modify_order,
    update_order_params,
    fetch_quotes,
)
from volstreet.angel_interface.active_session import ActiveSession
from volstreet.trade_interface import Index
from volstreet.strategies.strats import (
    intraday_strangle,
    delta_hedged_strangle,
    overnight_straddle,
    biweekly_straddle,
    buy_weekly_hedge,
    quick_strangle,
    reentry_straddle,
    trend_v2,
)


class BaseStrategy(ABC):
    def __init__(
        self,
        parameters,  # Note: The type is not specified, it can be list or dict
        indices: list[str],
        dtes: list[int],
        exposure: int | float = 0,  # This is not a compulsory parameter
        special_parameters: Optional[dict] = None,
        start_time: tuple = (9, 16),
        strategy_tags: Optional[list[str]] = None,
        client_data: Optional[dict] = None,
    ):
        self.exposure = exposure
        self.start_time = start_time
        self.client_data = {} if client_data is None else client_data
        self._strategy_tags = strategy_tags
        self._indices = indices
        self.dtes = dtes
        self._parameters = parameters
        self._special_parameters = special_parameters

        # Initialize attributes that will be set in `run`
        self.strategy_tags = None
        self.indices_to_trade = None
        self.parameters = None
        self.special_parameters = None
        self.strategy_threads = None

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"parameters="
            f"{self._truncate_or_str(self.parameters if self.parameters is not None else self._parameters)}, "
            f"indices={None if self.indices_to_trade is None else [index.name for index in self.indices_to_trade]}, "
            f"tags={self.strategy_tags if self.strategy_tags is not None else self._strategy_tags}, "
            f"client_data={self._truncate_or_str(self.client_data)})"
        )

    @staticmethod
    def _truncate_or_str(obj, max_len=50):
        s = str(obj)
        return s if len(s) <= max_len else s[:max_len] + "..."

    @property
    @abstractmethod
    def strats(self) -> list:
        pass

    @property
    @abstractmethod
    def to_divide_exposure(self) -> bool:
        pass

    @abstractmethod
    def set_strategy_tags(
        self, strategy_tags: Optional[list[str] | str] = None
    ) -> list[str]:
        pass

    @staticmethod
    def set_parameters(parameters, special_parameters):
        # Ensure parameters is a list of dictionaries
        parameters = [parameters] if isinstance(parameters, dict) else parameters

        # Ensure each item in special_parameters is a list of dictionaries
        special_parameters = {} if special_parameters is None else special_parameters
        if special_parameters:
            special_parameters = {
                key: [value] if isinstance(value, dict) else value
                for key, value in special_parameters.items()
            }

        return parameters, special_parameters

    def no_trade(self):
        notifier(
            f"No {self.__class__.__name__} trade today",
            self.client_data.get("webhook_url"),
        )

    def setup_thread(self, index: Index, tag: str, strategy) -> Thread:
        index_parameters = self.parameters[index.name][tag]
        tag_formatted = tag.lower().replace(" ", "_")
        return Thread(
            target=strategy,
            kwargs=index_parameters,
            name=f"{index.name}_{tag_formatted}".lower(),
        )

    def setup_threads(self, indices: list[Index]) -> list[Thread]:
        if len(indices) == 0:
            return [Thread(target=self.no_trade)]
        strategy_threads = [
            self.setup_thread(index, tag, strategy)
            for index in indices
            for tag, strategy in zip(self.strategy_tags, self.strats)
        ]
        return strategy_threads

    def initialize_parameters(self, parameters, special_parameters) -> dict:
        """Returns a dictionary of parameters for each index and strategy tag."""

        # Since this function is called after set_parameters, parameters is a list of dictionaries
        # It is also called after initialize_indices, so indices_to_trade is already set
        # We will use both of this information to set quantities if exposure is given
        if self.exposure:
            exposure = (
                self.exposure / len(self.indices_to_trade)
                if self.to_divide_exposure
                else self.exposure
            )
            for param in parameters:
                param["exposure"] = exposure

        # Add webhook url and strategy tag to each parameter dictionary
        for tag, param in zip(self.strategy_tags, parameters):
            param.update(
                {
                    "notification_url": self.client_data.get("webhook_url"),
                    "strategy_tag": tag,
                }
            )

        # Organize parameters by strategy tag
        param_by_tag = {
            tag: param for tag, param in zip(self.strategy_tags, parameters)
        }

        # Initialize final output dictionary
        final_parameters = {}

        # Iterate through each index to populate final_parameters
        for index in self.indices_to_trade:
            final_parameters[index.name] = {}

            # Initialize with base parameters and update the param with the underlying
            for tag in self.strategy_tags:
                param = param_by_tag[tag].copy()
                param.update({"underlying": index})
                final_parameters[index.name][tag] = param

            # Update with special parameters if available
            special_for_index = (
                special_parameters.get(index.name, []) if special_parameters else []
            )
            for tag, special_param in zip(self.strategy_tags, special_for_index):
                if special_param:
                    final_parameters[index.name][tag].update(special_param)
        logger.info(
            f"Initializing {self.__class__.__name__} with parameters: {final_parameters}"
        )
        return final_parameters

    def run(self):
        """This function will run the strategy. IMPORTANT: it will block until all threads are finished."""

        # Moved initialization methods here
        self.strategy_tags = self.set_strategy_tags(self._strategy_tags)
        self.indices_to_trade = initialize_indices(self, self._indices, self.dtes)
        self.parameters, self.special_parameters = self.set_parameters(
            self._parameters, self._special_parameters
        )
        self.parameters = self.initialize_parameters(
            self.parameters,
            self.special_parameters,
        )
        self.strategy_threads = self.setup_threads(self.indices_to_trade)

        logger.info(
            f"Waiting for {self.__class__.__name__} to start at {self.start_time}"
        )

        while current_time().time() < time(*self.start_time):
            sleep(1)

        # Start all threads
        for thread in self.strategy_threads:
            thread.start()

        # Join all threads
        for thread in self.strategy_threads:
            thread.join()


class QuickStrangle(BaseStrategy):
    @property
    def strats(self):
        return [quick_strangle]

    @property
    def to_divide_exposure(self) -> bool:
        return True

    def set_strategy_tags(self, strategy_tags: Optional[list[str]] = None) -> list[str]:
        return strategy_tags or ["Quick Strangle"]


class IntradayStrangle(BaseStrategy):
    @property
    def strats(self):
        return [intraday_strangle]

    @property
    def to_divide_exposure(self) -> bool:
        return True

    def set_strategy_tags(self, strategy_tags: Optional[list[str]] = None) -> list[str]:
        return strategy_tags or ["Intraday strangle"]


class TrendV2(BaseStrategy):
    @property
    def strats(self):
        return [trend_v2]

    @property
    def to_divide_exposure(self) -> bool:
        return True

    def set_strategy_tags(
        self, strategy_tags: Optional[list[str] | str] = None
    ) -> list[str]:
        return strategy_tags or ["Trend v2"]


class DeltaHedgedStrangle(BaseStrategy):
    @property
    def strats(self):
        return [delta_hedged_strangle]

    @property
    def to_divide_exposure(self) -> bool:
        return True

    def set_strategy_tags(
        self, strategy_tags: Optional[list[str] | str] = None
    ) -> list[str]:
        return strategy_tags or ["Delta hedged strangle"]


class ReentryStraddle(BaseStrategy):
    @property
    def strats(self):
        return [reentry_straddle]

    @property
    def to_divide_exposure(self) -> bool:
        return True

    def set_strategy_tags(
        self, strategy_tags: Optional[list[str] | str] = None
    ) -> list[str]:
        return strategy_tags or ["Reentry straddle"]


class OvernightStraddle(BaseStrategy):
    """Since the overnight straddle is a combination of two strategies (main and hedge),
    the parameters should be a list of two dictionaries. The first dictionary will be used
    for the main strategy and the second dictionary will be used for the hedge strategy.

    Similarly, the special parameters should be a dictionary of lists. The keys of the dictionary
    should be the index names and the values should be a list of two dictionaries. The first dictionary
    will be used for the main strategy and the second dictionary will be used for the hedge strategy.
    """

    @property
    def strats(self):
        return [buy_weekly_hedge, overnight_straddle]

    @property
    def to_divide_exposure(self) -> bool:
        return False

    def set_strategy_tags(
        self, strategy_tags: Optional[list[str] | str] = None
    ) -> list[str]:
        return strategy_tags or ["Weekly hedge", "Overnight short straddle"]


class BiweeklyStraddle(BaseStrategy):
    """Since the biweekly straddle is a combination of two strategies (main and hedge),
    the parameters should be a list of two dictionaries. The first dictionary will be used
    for the main strategy and the second dictionary will be used for the hedge strategy.

    Similarly, the special parameters should be a dictionary of lists. The keys of the dictionary
    should be the index names and the values should be a list of two dictionaries. The first dictionary
    will be used for the main strategy and the second dictionary will be used for the hedge strategy.
    """

    @property
    def strats(self):
        return [buy_weekly_hedge, biweekly_straddle]

    @property
    def to_divide_exposure(self) -> bool:
        return False

    def set_strategy_tags(
        self, strategy_tags: Optional[list[str] | str] = None
    ) -> list[str]:
        return strategy_tags or ["Biweekly hedge", "Biweekly straddle"]


class Client:
    strategy_function_map = {
        "quick_strangle": QuickStrangle,
        "intraday_strangle": IntradayStrangle,
        "overnight_straddle": OvernightStraddle,
        "biweekly_straddle": BiweeklyStraddle,
        "delta_hedged_strangle": DeltaHedgedStrangle,
        "reentry_straddle": ReentryStraddle,
        "trend_v2": TrendV2,
    }

    def __init__(
        self,
        user: str,
        pin: str,
        apikey: str,
        authkey: str,
        name: str = None,
        whatsapp: str = None,
        error_url: str = None,
        config_mode: str = "s3",
        webhook_urls: dict[str, str] = None,
    ):
        self.user = user
        self.pin = pin
        self.apikey = apikey
        self.authkey = authkey
        self.webhook_urls = webhook_urls or {}
        self.name = name
        self.strategies = []
        self.session_terminated: bool = False
        self.whatsapp = whatsapp
        self.error_url = error_url
        self.config_mode = config_mode

    @classmethod
    def from_name(cls, client: str, **kwargs) -> "Client":
        try:
            user = __import__("os").environ[f"{client}_USER"]
            pin = __import__("os").environ[f"{client}_PIN"]
            apikey = __import__("os").environ[f"{client}_API_KEY"]
            authkey = __import__("os").environ[f"{client}_AUTHKEY"]
        except KeyError:
            raise KeyError(
                f"Environment variables for {client} not found. Please check if the environment variables are set."
            )

        error_url = os.getenv(f"{client}_ERROR_URL", os.getenv("ERROR_URL", None))
        whatsapp = os.getenv(f"{client}_WHATSAPP", None)
        webhook_urls = {"default": os.getenv(f"{client}_WEBHOOK_URL", None)}
        return cls(
            user=user,
            pin=pin,
            apikey=apikey,
            authkey=authkey,
            name=client,
            whatsapp=whatsapp,
            error_url=error_url,
            webhook_urls=webhook_urls,
            **kwargs,
        )

    def set_webhook_urls_for_strats(self) -> None:
        for strategy in self.strategy_function_map.keys():
            try:
                self.webhook_urls[strategy] = __import__("os").environ[
                    f"{self.name}_WEBHOOK_URL_{strategy.upper()}"
                ]
            except KeyError:
                pass

    def login(self) -> None:
        login(
            self.user,
            self.pin,
            self.apikey,
            self.authkey,
            self.webhook_urls.get("default"),
        )
        set_error_notification_settings("url", self.error_url)
        set_error_notification_settings("whatsapp", self.whatsapp)

    def terminate(self) -> None:
        self.session_terminated = True
        LiveFeeds.close()
        ActiveSession.obj.terminateSession(self.user)

    def load_config_from_s3(self) -> list[dict]:
        try:
            s3 = boto3.client("s3", region_name="ap-south-1")
            client_info = json.loads(
                s3.get_object(
                    Bucket="userstrategies", Key=f"{self.name.lower()}/strategies.json"
                )["Body"]
                .read()
                .decode("utf-8")
            )
            return client_info
        except Exception as e:
            logger.error(f"Error in loading strategies for client {self.name}: {e}")
            raise e

    def load_strats(self) -> None:
        if self.config_mode == "s3":
            client_info = self.load_config_from_s3()
        else:
            with open("client_config.json", "r") as f:
                config_data = json.load(f)
            client_info = config_data[self.name]

        for strategy_data in client_info:
            strategy_class = self.strategy_function_map[strategy_data["type"]]
            webhook_url = self.webhook_urls.get(
                strategy_data["type"], self.webhook_urls.get("default")
            )
            strategy = strategy_class(
                **strategy_data["init_params"],
                client_data={"user": self.user, "webhook_url": webhook_url},
            )
            self.strategies.append(strategy)

    @wait_for_login
    def continuously_handle_open_orders(self):
        while not self.session_terminated:
            try:
                order_book = fetch_book("orderbook", from_api=True)
                if not order_book:
                    continue
                open_orders = get_open_orders(order_book, statuses=["open"])

                if open_orders.size > 0:
                    order_descriptions = [
                        {
                            "id": order["orderid"],
                            "symbol": order["tradingsymbol"],
                            "price": order["price"],
                        }
                        for order in open_orders
                    ]
                    logger.info(
                        f"Modifying open orders {order_descriptions} "
                        f"at {current_time()}"
                    )
                    modify_orders(open_orders)
            except Exception as e:
                logger.error(f"Error in continuously handling open orders: {e}")
            # In Python, the "finally" block is guaranteed to be executed regardless of how the try block is exited.
            # This includes situations where the try block is exited due to a return, break, or continue statement,
            # or even if an exception is raised. Hence, the lock gets released in the "finally" block.
            finally:
                sleep(3)


def run_client(
    client: Client,
    websockets: bool = True,
    price_socket_manager: Manager = None,
    order_socket_manager: Manager = None,
    notifier_level="INFO",
) -> None:
    # Setting notification settings
    client.set_webhook_urls_for_strats()
    set_notifier_level(notifier_level)
    client.login()

    # Load strategies
    client.load_strats()
    logger.info(
        f"Client {client.name} logged in successfully. Starting strategies with the following settings:\n"
        f"Notifier level: {config.NOTIFIER_LEVEL}\n"
        f"Error notification settings: {config.ERROR_NOTIFICATION_SETTINGS}"
    )

    # Wait for market to open
    start_time = current_time().replace(hour=9, minute=14, second=1)
    seconds_to_start = (start_time - current_time()).total_seconds()
    sleep(max(seconds_to_start, 0))

    # Starting order modification thread
    logger.info(
        f"Starting open orders handler in client {client.name} at {current_time()}..."
    )
    Thread(target=client.continuously_handle_open_orders).start()

    if websockets:
        # Starting live feeds
        logger.info(
            f"Starting live feeds in client {client.name} at {current_time()}..."
        )
        LiveFeeds.start_price_feed(price_socket_manager)
        LiveFeeds.start_order_feed(order_socket_manager)

    # Starting strategies
    strategy_threads = [Thread(target=strategy.run) for strategy in client.strategies]
    logger.info(f"Starting strategies in client {client.name} at {current_time()}")
    for strategy in strategy_threads:
        strategy.start()

    for strategy in strategy_threads:
        strategy.join()


def get_open_orders(
    order_book: list,
    order_ids: list[str] | tuple[str] | np.ndarray[str] = None,
    statuses: list[str] | tuple[str] | np.ndarray[str] = None,
):
    """Returns a list of open order ids. If order_ids is provided,
    it will return open orders only for those order ids. Otherwise,
    it will return all open orders where the ordertag is not empty.
    """
    if order_ids is None:
        order_ids = [
            order["orderid"] for order in order_book if order["ordertag"] != ""
        ]
    if statuses is None:
        statuses = ["open", "open pending", "modified", "modify pending"]
    open_orders_with_params: np.ndarray[dict] = lookup_and_return(
        order_book,
        ["orderid", "status"],
        [order_ids, statuses],
        config.modification_fields,
    )
    return open_orders_with_params


def modify_orders(open_orders_params: list[dict] | np.ndarray[dict]):
    quotes = fetch_quotes(
        [order["symboltoken"] for order in open_orders_params],
        structure="dict",
        from_source=True,
    )

    for order in open_orders_params:
        quote_data = quotes[order["symboltoken"]]
        modified_params = update_order_params(order, quote_data)

        try:
            modify_order(modified_params)
        except Exception as e:
            if isinstance(e, DataException):
                logger.error(f"Error in modifying order: {e}")
                sleep(1)


def add_env_vars_for_client(
    name: str,
    user: str,
    pin: str,
    api_key: str,
    auth_key: str,
    webhook_url: Optional[str] = None,
):
    # Specify the variable name and value
    var_dict = {
        f"{name}_USER": user,
        f"{name}_PIN": pin,
        f"{name}_API_KEY": api_key,
        f"{name}_AUTHKEY": auth_key,
    }

    if webhook_url is not None:
        var_dict[f"{name}_WEBHOOK_URL"] = webhook_url

    # Use the os.system method to set the system-wide environment variable
    for var_name, var_value in var_dict.items():
        os.system(f"setx {var_name} {var_value}")


def prepare_default_strategy_params(
    strategy_name: str,
    as_string: bool = False,
):
    init_params = get_default_params(BaseStrategy)
    strategy_params = get_default_params(eval(strategy_name))
    strategy_params.pop("client_data", None)
    strategy_params.pop("strategy_tag", None)
    init_params["parameters"] = strategy_params
    if as_string:
        return json.dumps(init_params)
    return init_params


def modify_strategy_params(
    client_config_data, client_name, strategy_name, init_params=None
):
    """
    Update the init_params of a specific strategy for a specific client in the given JSON data.
    Adds the client and/or strategy if they don't exist.

    Parameters:
    - json_data (dict): The original JSON data as a Python dictionary.
    - client_name (str): The name of the client to update.
    - strategy_name (str): The name of the strategy to update.
    - new_init_params (dict): The new init_params to set.

    Returns:
    - bool: True if the update/addition was successful, False otherwise.
    """

    if init_params is None:
        init_params = get_default_params(eval(strategy_name))

    # Search for the strategy for the client
    for strategy in client_config_data:
        if strategy["type"] == strategy_name:
            # Update the init_params
            strategy["init_params"].update(init_params)
            logger.info(f"Updated {strategy_name} for {client_name}.")
            return True

    # If strategy not found, add it
    logger.info(
        f"Strategy {strategy_name} not found for client {client_name}. Adding new strategy."
    )
    new_strategy = {"type": strategy_name, "init_params": init_params}
    client_config_data[client_name]["strategies"].append(new_strategy)

    return True


def get_default_params(obj, as_string=False):
    """
    Given a function, it returns a dictionary containing all the default
    keyword arguments and their values.
    """
    signature = inspect.signature(obj)
    params = {
        k: v.default if v.default is not inspect.Parameter.empty else None
        for k, v in signature.parameters.items()
    }
    # Remove the 'underlying' parameter if it exists
    params.pop("underlying", None)
    if as_string:
        return json.dumps(params)
    return params


def get_n_dte_indices(
    *indices: Index, dtes: list[int], safe: bool
) -> list[Index] | list[None]:
    safe_indices = ["NIFTY", "BANKNIFTY", "FINNIFTY"]

    time_to_expiries = {
        index: int(
            time_to_expiry(index.current_expiry, effective_time=True, in_days=True)
        )
        for index in indices
    }

    if 0 in dtes:
        dte0 = filter(lambda x: time_to_expiries.get(x) == 0, time_to_expiries)
    else:
        dte0 = []

    if any([dte >= 1 for dte in dtes]) and safe:
        dte_above_0 = filter(
            lambda x: time_to_expiries.get(x) in dtes and x.name in safe_indices,
            time_to_expiries,
        )

    elif any([dte >= 1 for dte in dtes]):
        dte_above_0 = filter(
            lambda x: time_to_expiries.get(x) in dtes, time_to_expiries
        )

    else:
        dte_above_0 = []

    eligible_indices = set(dte0).union(set(dte_above_0))

    return list(eligible_indices)


def initialize_indices(strategy, indices: list[str], dtes: list[int]) -> list[Index]:
    indices = [Index(index) for index in indices]
    # Hard coding safe indices for now. Lets wait for indices to mature
    indices: list[Index] | [] = get_n_dte_indices(*indices, dtes=dtes, safe=True)
    notify_indices_being_traded(strategy, indices)
    return indices


def notify_indices_being_traded(strategy, indices: list[Index]) -> None:
    if indices:
        notifier(
            f"Trading {strategy.__class__.__name__} on {', '.join([index.name for index in indices])}.",
            strategy.client_data.get("webhook_url"),
            "INFO",
        )
    else:
        notifier(
            f"No indices to trade for {strategy.__class__.__name__}.",
            strategy.client_data.get("webhook_url"),
            "INFO",
        )
