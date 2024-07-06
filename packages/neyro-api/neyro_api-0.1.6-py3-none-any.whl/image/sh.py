import requests
import json
import aiohttp

class ImageAPI:
    @staticmethod
    def sh(api, **kwargs):
        url = f"{api.BASE_URL}/image/sh"
        response = requests.post(url, headers=api.headers, data=json.dumps(kwargs))
        return response.json()

    @staticmethod
    async def async_sh(api, **kwargs):
        url = f"{api.BASE_URL}/image/sh"
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=api.headers, data=json.dumps(kwargs)) as response:
                return await response.json()