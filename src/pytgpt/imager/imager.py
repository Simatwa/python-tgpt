import requests
import os
from typing import Generator, Union
from string import punctuation
from random import choice
from random import randint


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
        self.session = requests.Session()
        self.session.proxies = proxies
        self.session.headers = self.headers
        self.timeout = timeout
        self.prompt: str = "AI-generated image - pytgpt"
        self.image_extension: str = "jpeg"

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
                resp = self.session.get(
                    url=self.image_gen_endpoint % dict(prompt=prompt + ads()),
                    timeout=self.timeout,
                )
                resp.raise_for_status()
                yield resp.content

        def for_non_stream():
            response = []

            for image in for_stream():
                response.append(image)
            return response

        self.prompt = prompt
        return for_stream() if stream else for_non_stream()

    def save(
        self,
        response: list[bytes],
        name: str = None,
        dir: str = os.getcwd(),
        filenames_prefix: str = "",
    ) -> list[str]:
        """Save generated images

        Args:
            response (list[bytes]|Generator): Response of Imager.generate
            name (str):  Filename for the images. Defaults to last prompt.
            dir (str, optional): Directory for saving images. Defaults to os.getcwd().
            filenames_prefix (str, optional): String to be prefixed at each filename to be returned.
        """
        assert isinstance(
            response, (list, Generator)
        ), f"Response should be of {list} or {Generator} types"
        name = self.prompt if name is None else name

        filenames: list = []

        for count, image in enumerate(response):

            def complete_path():
                count_value = "" if count == 0 else f"_{count}"
                return os.path.join(
                    dir, name + count_value + "." + self.image_extension
                )

            while os.path.isfile(complete_path()):
                count += 1

            absolute_path_to_file = complete_path()
            filenames.append(filenames_prefix + os.path.split(absolute_path_to_file)[1])

            with open(absolute_path_to_file, "wb") as fh:
                fh.write(image)

        return filenames


class Prodia(Imager):
    """
    This class provides methods for generating images based on prompts.
    """

    def __init__(self, timeout: int = 30, proxies: dict[str, str] = {}):
        """Constructor

        Args:
            timeout (int, optional): Http request timeout in seconds. Defaults to 30.
            proxies (dict[str, str], optional): Http request proxies. Defaults to {}.
        """
        super().__init__(timeout=timeout, proxies=proxies)
        self.image_extension: str = "png"

    def _generate(self, prompt: str) -> bytes:
        """
        Create a new image generation based on the given prompt.

        Args:
            prompt (str): The prompt for generating the image.

        Returns:
            resp (bytes): The generated image content
        """

        try:
            resp = self.session.get(
                "https://api.prodia.com/generate",
                params={
                    "new": "true",
                    "prompt": prompt,
                    "model": "dreamshaper_6BakedVae.safetensors [114c8abb]",
                    "negative_prompt": "(nsfw:1.5),verybadimagenegative_v1.3, ng_deepnegative_v1_75t, (ugly face:0.5),cross-eyed,sketches, (worst quality:2), (low quality:2.1), (normal quality:2), lowres, normal quality, ((monochrome)), ((grayscale)), skin spots, acnes, skin blemishes, bad anatomy, DeepNegative, facing away, tilted head, {Multiple people}, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worstquality, low quality, normal quality, jpegartifacts, signature, watermark, username, blurry, bad feet, cropped, poorly drawn hands, poorly drawn face, mutation, deformed, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, extra fingers, fewer digits, extra limbs, extra arms,extra legs, malformed limbs, fused fingers, too many fingers, long neck, cross-eyed,mutated hands, polar lowres, bad body, bad proportions, gross proportions, text, error, missing fingers, missing arms, missing legs, extra digit, extra arms, extra leg, extra foot, repeating hair",
                    "steps": "50",
                    "cfg": "9.5",
                    "seed": randint(1, 10000),
                    "sampler": "Euler",
                    "aspect_ratio": "square",
                },
                timeout=self.timeout,
            )
            data = resp.json()
            while True:
                resp = self.session.get(
                    f"https://api.prodia.com/job/{data['job']}", timeout=self.timeout
                )
                json = resp.json()
                if json["status"] == "succeeded":
                    return self.session.get(
                        f"https://images.prodia.xyz/{data['job']}.png?download=1",
                        timeout=self.timeout,
                    ).content

        except Exception as e:
            raise Exception("Unable to generate image") from e

    def generate(
        self,
        prompt: str,
        amount: int = 1,
        stream: bool = False,
        additives: bool = False,
    ) -> list[bytes]:
        """Generat image from prompt

        Args:
            prompt (str): Image description.
            amount (int): Total images to be generated. Defaults to 1.
            additives (bool, optional): Try to make each prompt unique. Defaults to True.

        Returns:
            list[bytes]|bytes: Image generated
        """
        self.prompt = prompt
        get_prompt: object = lambda prompt: (
            f"prompt {randint(1, 10000)}" if additives else prompt
        )

        def for_stream():
            for _ in range(amount):
                yield self._generate(get_prompt(prompt))

        def for_non_stream():
            resp = []
            for _ in range(amount):
                resp.append(self._generate(get_prompt(prompt)))
            return resp

        return for_stream() if stream else for_non_stream()


if __name__ == "__main__":
    bot = Prodia()
    resp = bot.generate("Coding bot ", 3, stream=True)
    bot.save(resp)
