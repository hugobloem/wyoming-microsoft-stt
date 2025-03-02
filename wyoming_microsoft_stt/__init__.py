"""Wyoming server for Microsoft STT."""

from typing import Literal
from pydantic import BaseModel


class SpeechConfig(BaseModel):
    """Speech configuration."""

    subscription_key: str
    service_region: str
    profanity: Literal["off", "masked", "removed"] = "masked"
    language: str = "en-US"
    realtime: bool = True
