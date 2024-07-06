import requests
import json
import aiohttp

class TextAPI:
    @staticmethod
    def gpt_new(api, **kwargs):
        url = f"{api.BASE_URL}/text/gpt-new"
        response = requests.post(url, headers=api.headers, data=json.dumps(kwargs))
        return response.json()

    @staticmethod
    async def async_gpt_new(api, **kwargs):
        url = f"{api.BASE_URL}/text/gpt-new"
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=api.headers, data=json.dumps(kwargs)) as response:
                return await response.json()