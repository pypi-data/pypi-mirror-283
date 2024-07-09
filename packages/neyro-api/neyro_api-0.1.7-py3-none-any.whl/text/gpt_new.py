import httpx
import json

class TextAPI:
    @staticmethod
    def gpt_new(api, **kwargs):
        url = f"{api.BASE_URL}/text/gpt-new"
        response = httpx.post(url, headers=api.headers, data=json.dumps(kwargs))
        response.raise_for_status()
        return response.json()

    @staticmethod
    async def async_gpt_new(api, **kwargs):
        url = f"{api.BASE_URL}/text/gpt-new"
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=api.headers, data=json.dumps(kwargs))
            response.raise_for_status()
            return response.json()
