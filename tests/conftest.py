"""Fixtures for tests."""

from types import SimpleNamespace
import pytest
import os


@pytest.fixture
def microsoft_stt_args():
    """Return MicrosoftSTT instance."""
    args = SimpleNamespace(
        subscription_key=os.environ.get("SPEECH_KEY"),
        service_region=os.environ.get("SPEECH_REGION"),
    )
    return args
