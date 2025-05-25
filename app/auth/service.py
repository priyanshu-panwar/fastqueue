from fastapi import Request
from app.auth.exceptions import InvalidAPIKeyException
from app.settings import settings

API_KEY = settings.api_key


def verify_api_key(request: Request):
    """
    Verify the API key from the request headers.
    Raises InvalidAPIKeyException if the API key is missing or invalid.
    """
    if settings.debug:
        # In debug mode, skip API key verification
        return None

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise InvalidAPIKeyException()

    api_key = auth_header.removeprefix("Bearer ").strip()
    if api_key != API_KEY:
        raise InvalidAPIKeyException()

    return api_key
