import httpx
import json

class NeyroAPI:
    BASE_URL = "https://api.neyrogen.online"

    def __init__(self, api_key, captcha_key):
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "x-captcha-token": captcha_key
        }

    def text_gpt_new(self, **kwargs):
        from .text.gpt_new import TextAPI
        return TextAPI.gpt_new(self, **kwargs)

    def image_sh(self, **kwargs):
        from .image.sh import ImageAPI
        return ImageAPI.sh(self, **kwargs)

    def audio_tts(self, **kwargs):
        from .audio.tts import AudioAPI
        return AudioAPI.tts(self, **kwargs)
