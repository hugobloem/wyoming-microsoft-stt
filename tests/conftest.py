"""Fixtures for tests."""

from wyoming_microsoft_stt import SpeechConfig
import pytest
import os


@pytest.fixture
def microsoft_stt_args():
    """Return MicrosoftSTT instance."""
    args = SpeechConfig(
        subscription_key=os.environ.get("SPEECH_KEY"),
        service_region=os.environ.get("SPEECH_REGION"),
    )
    return args
