import g4f
from .main import GPT4FREE
from pathlib import Path
from pytgpt.utils import default_path
from json import dump, load
from time import time
from threading import Thread as thr
from functools import wraps
from rich.progress import Progress
import logging

results_path = Path(default_path) / "provider_test.json"


def exception_handler(func):

    @wraps(func)
    def decorator(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            pass

    return decorator


@exception_handler
def is_working(provider: str) -> bool:
    """Test working status of a provider

    Args:
        provider (str): Provider name

    Returns:
        bool: is_working status
    """
    bot = GPT4FREE(provider=provider, is_conversation=False)
    text = bot.chat("hello")
    assert isinstance(text, str)
    assert bool(text.strip())
    assert "</" not in text
    assert ":" not in text
    assert len(text) > 2
    return True


class TestProviders:

    def __init__(
        self,
        test_at_once: int = 5,
        quiet: bool = False,
        timeout: int = 20,
        selenium: bool = False,
        do_log: bool = True,
    ):
        """Constructor

        Args:
            test_at_once (int, optional): Test n providers at once. Defaults to 5.
            quiet (bool, optinal): Disable stdout. Defaults to False.
            timout (int, optional): Thread timeout for each provider. Defaults to 20.
            selenium (bool, optional): Test even selenium dependent providers. Defaults to False.
            do_log (bool, optional): Flag to control logging. Defaults to True.
        """
        self.test_at_once: int = test_at_once
        self.quiet = quiet
        self.timeout = timeout
        self.do_log = do_log
        self.__logger = logging.getLogger(__name__)
        self.working_providers: list = [
            provider.__name__
            for provider in g4f.Provider.__providers__
            if provider.working
        ]

        if not selenium:
            import g4f.Provider.selenium as selenium_based
            from g4f import webdriver

            webdriver.has_requirements = False
            selenium_based_providers: list = dir(selenium_based)
            for provider in self.working_providers:
                try:
                    selenium_based_providers.index(provider)
                except ValueError:
                    pass
                else:
                    self.__log(
                        10, f"Dropping provider - {provider} - [Selenium dependent]"
                    )
                    self.working_providers.remove(provider)

        self.results_path: Path = results_path
        self.__create_empty_file(ignore_if_found=True)
        self.results_file_is_empty: bool = False

    def __log(
        self,
        level: int,
        message: str,
    ):
        """class logger"""
        if self.do_log:
            self.__logger.log(level, message)
        else:
            pass

    def __create_empty_file(self, ignore_if_found: bool = False):
        if ignore_if_found and self.results_path.is_file():
            return
        with self.results_path.open("w") as fh:
            dump({"results": []}, fh)
        self.results_file_is_empty = True

    def test_provider(self, name: str):
        """Test each provider and save successful ones

        Args:
            name (str): Provider name
        """

        try:
            bot = GPT4FREE(provider=name, is_conversation=False)
            start_time = time()
            text = bot.chat("hello there")
            assert isinstance(text, str), "Non-string response returned"
            assert bool(text.strip()), "Empty string"
            assert "</" not in text, "Html code returned."
            assert ":" not in text, "Json formatted response returned"
            assert len(text) > 2
        except Exception as e:
            pass
        else:
            self.results_file_is_empty = False
            with self.results_path.open() as fh:
                current_results = load(fh)
            new_result = dict(time=time() - start_time, name=name)
            current_results["results"].append(new_result)
            self.__log(20, f"Test result - {new_result['name']} - {new_result['time']}")

            with self.results_path.open("w") as fh:
                dump(current_results, fh)

    @exception_handler
    def main(
        self,
    ):
        self.__create_empty_file()
        threads = []
        # Create a progress bar
        total = len(self.working_providers)
        with Progress() as progress:
            self.__log(
                20, f"Testing {total} providers : {', '.join(self.working_providers)}"
            )
            task = progress.add_task(
                f"[cyan]Testing...[{self.test_at_once}]",
                total=total,
                visible=self.quiet == False,
            )
            while not progress.finished:
                for count, provider in enumerate(self.working_providers, start=1):
                    t1 = thr(
                        target=self.test_provider,
                        args=(provider,),
                    )
                    t1.start()
                    if count % self.test_at_once == 0 or count == len(provider):
                        for t in threads:
                            try:
                                t.join(self.timeout)
                            except Exception as e:
                                pass
                        threads.clear()
                    else:
                        threads.append(t1)
                    progress.update(task, advance=1)

    def get_results(self, run: bool = False, best: bool = False) -> list[dict]:
        """Get test results

        Args:
            run (bool, optional): Run the test first. Defaults to False.
            best (bool, optional): Return name of the best provider. Defaults to False.

        Returns:
            list[dict]|str: Test results.
        """
        if run or self.results_file_is_empty:
            self.main()

        with self.results_path.open() as fh:
            results: dict = load(fh)

        results = results["results"]
        if not results:
            if run:
                raise Exception("Unable to find working g4f provider")
            else:
                self.__log(30, "Hunting down working g4f providers.")
                return self.get_results(run=True, best=best)

        time_list = []

        sorted_list = []
        for entry in results:
            time_list.append(entry["time"])

        time_list.sort()

        for time_value in time_list:
            for entry in results:
                if entry["time"] == time_value:
                    sorted_list.append(entry)
        return sorted_list[0]["name"] if best else sorted_list

    @property
    def best(self):
        """Fastest provider overally"""
        return self.get_results(run=False, best=True)

    @property
    def auto(self):
        """Best working provider"""
        for result in self.get_results(run=False, best=False):
            self.__log(20, "Confirming working status of provider : " + result["name"])
            if is_working(result["name"]):
                return result["name"]
