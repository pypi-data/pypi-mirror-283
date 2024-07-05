from abc import ABC, abstractmethod
from dotenv import load_dotenv
import warnings
from typing import Dict
import inspect

from base.base_driver import BaseDriver
from base.wait import MyBy

# looding all env variables and ignoring a certain warning
load_dotenv()
warnings.filterwarnings("ignore", message="Worksheet.update.*method signature will change.*")


class StateInterface(ABC):
    """
    An abstract class for all the state interface classes
    """

    param: Dict[str, any] = {}

    def __init__(self, base: BaseDriver) -> None:
        self.__bd = base

    @property
    def bd(self):
        return self.__bd

    @classmethod
    def updateParam(cls, func):
        sig = inspect.signature(func)
        default_kwargs = {k: v.default for k, v in sig.parameters.items() if v.default != inspect.Parameter.empty}

        def wrapper(*args, **kwargs):
            cls.param.clear()
            combined_params = default_kwargs.copy()
            default_keys = combined_params.keys()
            specified_keys = kwargs.keys()
            positional_keys = list(sig.parameters.keys())[1:]
            for i, key in enumerate(positional_keys):
                if key not in default_keys:  # when it's an arg
                    if key in specified_keys:
                        combined_params[key] = kwargs[key]
                    else:
                        combined_params[key] = args[i + 1]
                else:  # when it's a kwarg
                    if key in specified_keys:
                        combined_params[key] = kwargs[key]
                    else:
                        if len(args) > (i + 1):
                            combined_params[key] = args[i + 1]
                cls.param[key] = combined_params[key]

            return func(*[args[0]], **combined_params)

        return wrapper


class Page(ABC):
    """A parent class of all specific page classes."""

    def __init__(self, base: BaseDriver) -> None:
        self.__bd = base
        self.jpnFormats = ["jpn", "japan", "japanese", "jp"]
        self.engFormats = ["eng", "english", "en"]
        self.emptyFormats = ["", "-", "<blank>", "<empty>", "blank", "empty"]
        self.anyFormats = ["anything", "dc", "Any", "any"]
        self.spaceFormats = ["<space>"]

    @property
    def bd(self):
        return self.__bd

    @abstractmethod
    def changeState(self):
        pass

    @abstractmethod
    def resetState(self):
        pass


class Locator:
    """A parent class of all page locator classes."""

    def __init__(self, base: BaseDriver) -> None:
        self.__bd = base
        self.by = MyBy()

    @property
    def bd(self):
        return self.__bd
