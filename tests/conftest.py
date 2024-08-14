"""Fixtures for tests."""

from types import SimpleNamespace
import pytest
from wyoming_microsoft_stt.microsoft_stt import MicrosoftSTT
import os


@pytest.fixture
def microsoft_stt():
    """Return MicrosoftSTT instance."""
    args = SimpleNamespace(
        subscription_key=os.environ.get("SPEECH_KEY"),
        service_region=os.environ.get("SPEECH_REGION"),
    )
    return MicrosoftSTT(args)
