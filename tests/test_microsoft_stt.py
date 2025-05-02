"""Tests for the MicrosoftTTS class."""

from wyoming_microsoft_stt.microsoft_stt import MicrosoftSTT


def test_initialize(microsoft_stt_args):
    """Test initialization."""
    microsoft_stt = MicrosoftSTT(microsoft_stt_args)
    assert microsoft_stt.speech_config is not None


def test_set_profanity(microsoft_stt_args):
    """Test set_profanity."""
    microsoft_stt = MicrosoftSTT(microsoft_stt_args)
    assert microsoft_stt.speech_config is not None

    profanity = "masked"
    microsoft_stt.set_profanity(profanity)
    # There is currently no way to check the set profanity level
