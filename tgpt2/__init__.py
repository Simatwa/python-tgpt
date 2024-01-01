from .tgpt2 import TGPT
from .imager import Imager

__version__ = "0.0.4"
__author__ = "Smartwa"
__repo__ = "https://github.com/Simatwa/python-tgpt2"

all = ["TGPT", "Imager"]

import warnings

warnings.simplefilter("once", category=DeprecationWarning)

warnings.warn(
    "This project has transitioned from being maintained under `tgpt2` to `python-tgpt` in response to a raised concern detailed at https://github.com/aandrew-me/tgpt/issues/180",
    DeprecationWarning,
)
