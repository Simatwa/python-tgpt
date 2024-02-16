import requests
import os
from typing import Generator
from string import punctuation
from random import choice

session = requests.Session()


class Imager:
    def __init__(
        self,
        timeout: int = 20,
        proxies: dict = {},
    ):
        """Initializes `Imager`

        Args:
            timeout (int, optional): Http request timeout. Defaults to 20.
            proxies (dict, optional): Http request proxies (socks). Defaults to {}.
        """
        self.image_gen_endpoint: str = "https://image.pollinations.ai/prompt/%(prompt)s"
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0",
        }
        session.proxies = proxies
        session.timeout = timeout
        self.__prompt: str = "AI-generated image - pytgpt"

    def generate(
        self, prompt: str, amount: int = 1, stream: bool = False, additives: bool = True
    ) -> list[bytes]:
        """Generat image from prompt

        Args:
            prompt (str): Image description.
            amount (int): Total images to be generated. Defaults to 1.
            additives (bool, optional): Try to make each prompt unique. Defaults to True.

        Returns:
            list[bytes]|bytes: Image generated
        """
        assert bool(prompt), "Prompt cannot be null"
        assert isinstance(
            amount, int
        ), f"Amount should be an integer only not {type(amount)}"
        assert amount > 0, "Amount should be greater than 0"
        ads = lambda: (
            ""
            if not additives
            else choice(punctuation)
            + choice(punctuation)
            + choice(punctuation)
            + choice(punctuation)
            + choice(punctuation)
        )

        def for_stream():
            for _ in range(amount):
                resp = session.get(
                    url=self.image_gen_endpoint % dict(prompt=prompt + ads())
                )
                resp.raise_for_status()
                yield resp.content

        def for_non_stream():
            response = []

            for image in for_stream():
                response.append(image)
            return response

        self.__prompt = prompt
        return for_stream() if stream else for_non_stream()

    def save(
        self, response: list[bytes], name: str = None, dir: str = os.getcwd()
    ) -> None:
        """Save generated images

        Args:
            response (list[bytes]|Generator): Response of Imager.generate
            name (str):  Filename for the images. Defaults to last prompt.
            dir (str, optional): Directory for saving images. Defaults to os.getcwd().
        """
        assert isinstance(
            response, (list, Generator)
        ), f"Response should be of {list} or {Generator} types"
        name = self.__prompt if name is None else name

        for count, image in enumerate(response):

            def complete_path():
                count_value = "" if count == 0 else f"_{count}"
                return os.path.join(dir, name + count_value + "." + "jpeg")

            while os.path.isfile(complete_path()):
                count += 1

            with open(complete_path(), "wb") as fh:
                fh.write(image)


if __name__ == "__main__":
    bot = Imager()
    resp = bot.generate("Coding bot ", 3, stream=True)
    bot.save(resp)
