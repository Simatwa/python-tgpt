__all__ = [
    "v1",
]

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from pytgpt import __version__
from pytgpt.utils import api_static_dir
from pydantic import BaseModel
from datetime import datetime, UTC
from . import v1

app = FastAPI(
    title="python-tgpt",
    summary="Interact with AI without API key",
    description=(
        "For **text** generation, **text-to-image** and **text-to-audio** conversions."
        "\n\n"
        "Access redoc at [/redoc](/redoc) endpoint."
        "\n\n"
        "Other documentation is available at official repo : [Simatwa/python-tgpt](https://github.com/Simatwa/python-tgpt)."
    ),
    version=__version__,
    contact={
        "name": "Smartwa",
        "email": "simatwacaleb@proton.me",
        "url": "https://simatwa.vercel.app",
    },
    license_info={
        "name": "GNU v3",
        "url": "https://github.com/Simatwa/python-tgpt/blob/main/LICENSE?raw=true",
    },
)


class ServerStatus(BaseModel):
    is_alive: bool = True
    as_at: datetime


@app.get("/", name="redirect-to-docs")
async def home():
    """Redirect to docs"""
    return RedirectResponse("/docs")


@app.get("/status", tags=["status"])
async def server_status() -> ServerStatus:
    """Server running status
    - `is_alive` : status
    - `as_at` : Time checked.
    """
    return ServerStatus(as_at=datetime.now(UTC))


app.include_router(v1.app, prefix="/v1", tags=["v1"])

app.mount("/static", StaticFiles(directory=api_static_dir), name="static")
