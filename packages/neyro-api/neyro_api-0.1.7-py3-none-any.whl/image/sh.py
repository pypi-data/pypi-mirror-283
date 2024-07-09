import httpx
import json

class ImageAPI:
    @staticmethod
    def sh(api, **kwargs):
        url = f"{api.BASE_URL}/image/sh"
        response = httpx.post(url, headers=api.headers, data=json.dumps(kwargs))
        response.raise_for_status()
        return response.json()

    @staticmethod
    async def async_sh(api, **kwargs):
        url = f"{api.BASE_URL}/image/sh"
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=api.headers, data=json.dumps(kwargs))
            response.raise_for_status()
            return response.json()
