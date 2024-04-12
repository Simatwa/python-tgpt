__all__ = [
    "v1",
]

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from pytgpt import __version__
from pydantic import BaseModel
from datetime import datetime
from . import v1

app = FastAPI(
    title="python-tgpt",
    summary="Interact with AI without API key",
    description="For full documentation visit official repo at [Simatwa/python-tgpt](https://github.com/Simatwa/python-tgpt).",
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


@app.get("/status", tags=["status"])
async def server_status() -> ServerStatus:
    """Server running status
    - `is_alive` : status
    - `as_at` : Time checked.
    """
    return ServerStatus(as_at=datetime.utcnow())


app.include_router(v1.app, prefix="/v1", tags=["v1"])
