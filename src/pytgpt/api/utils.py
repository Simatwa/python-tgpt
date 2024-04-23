from functools import wraps
from typing import Callable
from fastapi import HTTPException, status
from requests.exceptions import ProxyError, InvalidProxyURL, SSLError

get_exception_string: str = lambda e: (
    e.args[1] if e.args and len(e.args) > 1 else str(e)
)


def api_exception_handler(func: Callable):
    """Auto-handles common exceptions raised accordingly including proxy related.

    Args:
        func (Callable): FastAPI endpoint
    """

    @wraps(func)
    async def decorator(*args, **kwargs):
        try:
            return await func(*args, **kwargs)

        except (ProxyError, InvalidProxyURL, SSLError) as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=dict(message=f"Proxy related error. {get_exception_string(e)}"),
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=dict(message=get_exception_string(e)),
            )

    return decorator
