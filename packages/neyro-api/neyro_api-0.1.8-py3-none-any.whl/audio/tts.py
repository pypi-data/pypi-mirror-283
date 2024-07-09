import httpx
import json

class AudioAPI:
    @staticmethod
    def tts(api, **kwargs):
        url = f"{api.BASE_URL}/audio/tts"
        response = httpx.post(url, headers=api.headers, data=json.dumps(kwargs))
        response.raise_for_status()
        return response.json()

    @staticmethod
    async def async_tts(api, **kwargs):
        url = f"{api.BASE_URL}/audio/tts"
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=api.headers, data=json.dumps(kwargs))
            response.raise_for_status()
            return response.json()
