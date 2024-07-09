import httpx
import json

class AsyncNeyroAPI:
    BASE_URL = "https://api.neyrogen.online"

    def __init__(self, api_key, captcha_key):
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "x-captcha-token": captcha_key
        }

    async def text_gpt_new(self, **kwargs):
        from .text.gpt_new import TextAPI
        return await TextAPI.async_gpt_new(self, **kwargs)

    async def image_sh(self, **kwargs):
        from .image.sh import ImageAPI
        return await ImageAPI.async_sh(self, **kwargs)

    async def audio_tts(self, **kwargs):
        from .audio.tts import AudioAPI
        return await AudioAPI.async_tts(self, **kwargs)
