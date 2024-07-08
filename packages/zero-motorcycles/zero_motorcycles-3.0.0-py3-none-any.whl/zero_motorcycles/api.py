"""Sample API Client."""

from __future__ import annotations

import base64
import json
import socket
from hashlib import md5
from typing import Any

import aiohttp
import async_timeout
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad

from .model import Unit, Zero, Expire


class ZeroApiError(Exception):
    """Exception to indicate a general API error."""


class ZeroApiCommunicationError(
    ZeroApiError,
):
    """Exception to indicate a communication error."""


class ZeroApiAuthenticationError(
    ZeroApiError,
):
    """Exception to indicate an authentication error."""


def _verify_response_or_raise(response: aiohttp.ClientResponse) -> None:
    """Verify that the response is valid."""
    if response.status == 601:
        raise ZeroApiAuthenticationError("Invalid credentials")
    response.raise_for_status()


class ZeroApiClient:
    """Sample API Client."""

    API_URL = "https://api-us-cypherstore-prod.zeromotorcycles.com/starcom/v1"
    ENCRYPTION_KEY = "8FA043AADEC92367108D0E25D2C6064F"
    SOURCE = "zero"
    FORMAT = "json"

    def __init__(
        self,
        username: str,
        password: str,
        session: aiohttp.ClientSession | None = None,
    ) -> None:
        """Sample API Client."""
        self._username = username
        self._password = password
        self._session = session if session is not None else aiohttp.ClientSession()

    async def async_get_units(self) -> Any:
        data = {"commandname": "get_units"}

        response = await self._api_wrapper(method="post", data=data)
        return [Unit(**unit) for unit in response]

    async def async_get_last_transmit(self, unit) -> Zero:
        data = {"unitnumber": unit, "commandname": "get_last_transmit"}

        response = await self._api_wrapper(method="post", data=data)
        model = Zero(**response[0])
        return model

    async def async_get_expiration_date(self, unit) -> Any:
        data = {"unitnumber": unit, "unittype": 5, "commandname": "get_expiration_date"}

        response = await self._api_wrapper(method="post", data=data)
        return Expire(**response)

    async def _api_wrapper(
        self,
        method: str,
        url: str | None = None,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> Any:
        """Get information from the API."""
        if url is None:
            url = self.API_URL

        body = {"data": self._encrypt(data)}

        try:
            async with async_timeout.timeout(10):
                response = await self._session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=body,
                )
                _verify_response_or_raise(response)
                return await response.json()

        except TimeoutError as exception:
            msg = f"Timeout error fetching information - {exception}"
            raise ZeroApiCommunicationError(
                msg,
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            msg = f"Error fetching information - {exception}"
            raise ZeroApiCommunicationError(
                msg,
            ) from exception
        except Exception as exception:  # pylint: disable=broad-except
            msg = f"Something really wrong happened! - {exception}"
            raise ZeroApiError(
                msg,
            ) from exception

    def _encrypt(self, data: dict[str, Any]) -> str:
        # Add some additional keys to the JSON body
        data["format"] = self.FORMAT
        data["source"] = self.SOURCE
        data["user"] = self._username
        data["pass"] = self._password

        # from https://stackoverflow.com/a/36780727
        message = json.dumps(data).encode()
        salt = get_random_bytes(8)
        key_iv = self._bytes_to_key(self.ENCRYPTION_KEY.encode(), salt)
        key = key_iv[:32]
        iv = key_iv[32:]
        aes = AES.new(key, AES.MODE_CBC, iv)
        return base64.b64encode(
            b"Salted__" + salt + aes.encrypt(pad(message, AES.block_size))
        ).decode()

    @staticmethod
    def _bytes_to_key(data, salt, output=48):
        # from https://stackoverflow.com/a/36780727
        # extended from https://gist.github.com/gsakkis/4546068
        assert len(salt) == 8, len(salt)
        data += salt
        key = md5(data).digest()
        final_key = key
        while len(final_key) < output:
            key = md5(key + data).digest()
            final_key += key
        return final_key[:output]
