from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from functools import wraps
import inspect
from typing import Dict

from utils.wrapper import Wrapper


class MyBy:
    """
    Provides keys that each links to an 'By' object.
    The purpose is to have control to By objects name.

    For example:
    If we want to rename one of the keys, that can be done by renaming it just in here.
    Of course do not forget to use F2 before renaming it, so it applies to all references.
    """

    xpath = By.XPATH
    css = By.CSS_SELECTOR
    cname = By.CLASS_NAME
    id = By.ID
    link = By.LINK_TEXT
    plink = By.PARTIAL_LINK_TEXT
    name = By.NAME
    tag = By.TAG_NAME


class WaitDriver:
    """
    Provides explicit wait, i.e. will wait until either the element has found or exceed time limit.
    """

    def __init__(self, driver, duration: int) -> None:
        self.init_duration = duration
        self.wdw = WebDriverWait(driver, duration)

    def waitConfig(func):
        sig = inspect.signature(func)
        default_kwargs = {k: v.default for k, v in sig.parameters.items() if v.default != inspect.Parameter.empty}

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            # update parameters
            combined_params = default_kwargs.copy()
            default_keys = combined_params.keys()
            specified_keys = kwargs.keys()
            positional_keys = list(sig.parameters.keys())[1:]
            for i, key in enumerate(positional_keys):
                if key not in default_keys:  # when it's an arg
                    if key in specified_keys:
                        combined_params[key] = kwargs[key]
                    else:
                        combined_params[key] = args[i]
                else:  # when it's a kwarg
                    if key in specified_keys:
                        combined_params[key] = kwargs[key]
                    else:
                        if len(args) > i:
                            combined_params[key] = args[i]
            # update config values
            if combined_params["cusdur"] > 0:
                self.wdw._timeout = combined_params["cusdur"]
            if combined_params["cusfreq"] != 0.5:
                self.wdw._poll = combined_params["cusfreq"]
            # wait for the staleness (absence) of the specified element
            if combined_params["staleness_element"]:
                self.wdw.until(EC.staleness_of(combined_params["staleness_element"]))
            # invoke the function
            res = func(self, **combined_params)
            # reset config values
            self.wdw._timeout = self.init_duration
            self.wdw._poll = 0.5
            return res

        return wrapper

    @waitConfig
    def all_elements(self, by: MyBy, locator, staleness_element=None, cusdur: float = 0, cusfreq: float = 0.5) -> list[WebElement]:
        res = self.wdw.until(EC.presence_of_all_elements_located((by, locator)))
        return res

    @waitConfig
    def an_element(self, by: MyBy, locator, staleness_element=None, cusdur: float = 0, cusfreq: float = 0.5) -> WebElement:
        res = self.wdw.until(EC.presence_of_element_located((by, locator)))
        return res

    @waitConfig
    def clickable(self, by: MyBy, locator, staleness_element=None, cusdur: float = 0, cusfreq: float = 0.5) -> WebElement:
        res = self.wdw.until(EC.element_to_be_clickable((by, locator)))
        return res

    @waitConfig
    def invisible(self, by: MyBy, locator, staleness_element=None, cusdur: float = 0, cusfreq: float = 0.5) -> bool:
        res = self.wdw.until(EC.invisibility_of_element_located((by, locator)))
        return res

    @waitConfig
    def visible(self, by: MyBy, locator, staleness_element=None, cusdur: float = 0, cusfreq: float = 0.5) -> WebElement:
        res = self.wdw.until(EC.visibility_of_element_located((by, locator)))
        return res
