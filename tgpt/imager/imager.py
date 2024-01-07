import requests
import json

session = requests.Session()


class Imager:
    def __init__(
        self,
        negative_prompt: str = "",
        version: str = "c4ue22fb7kb6wlac",
        model: str = "photo",
        token: str = None,
        proxies: dict = {},
    ):
        """Initializes `Imager`

        Args:
            negative_prompt (str, optional): Negative prompt. Defaults to "".
            version (str, optional): Version name. Defaults to "c4ue22fb7kb6wlac".
            model (str, optional): Generation model. Defaults to 'photo'.
            token (str, optional): API token. Defaults to None.
            proxies (dict, optional): Http request proxies (socks). Defaults to {}.
        """
        self.token = token
        self.model = model
        self.negative_prompt = negative_prompt
        self.version = version
        self.image_gen_endpoint = "https://api.craiyon.com/v3"
        self.image_down_endpoint = "https://img.craiyon.com/"
        self.headers = {
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/110.0",
        }
        session.proxies = proxies

    def generate(self, prompt: str) -> dict:
        """Generat image from prompt

        Args:
            prompt (str): Image description

        Returns:
            dict: Response `url`
        """
        session.headers.update(self.headers)
        payload = {
            "token": self.token,
            "model": self.model,
            "negative_prompt": self.negative_prompt,
            "version": self.version,
            "prompt": prompt,
        }

        response = session.post(self.image_gen_endpoint, json=payload)
        # out = lambda data: print(json.dumps(dict(data), indent=4))
        # out(response.headers)
        try:
            pass
            # out(response.json())
        except:
            pass
        return response.text


if __name__ == "__main__":
    bot = Imager()
    resp = bot.generate("Vehicle on road")
    print(resp)
