import requests
import json
import aiohttp

class AudioAPI:
    @staticmethod
    def tts(api, **kwargs):
        url = f"{api.BASE_URL}/audio/tts"
        response = requests.post(url, headers=api.headers, data=json.dumps(kwargs))
        return response.json()

    @staticmethod
    async def async_tts(api, **kwargs):
        url = f"{api.BASE_URL}/audio/tts"
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=api.headers, data=json.dumps(kwargs)) as response:
                return await response.json()