"""Tests for the MicrosoftTTS class."""

from wyoming_microsoft_stt.microsoft_stt import MicrosoftSTT


def test_initialize(microsoft_stt_args):
    """Test initialization."""
    microsoft_stt = MicrosoftSTT(microsoft_stt_args)
    assert microsoft_stt.speech_config is not None


def test_transcribe(microsoft_stt_args):
    """Test synthesize."""
    microsoft_stt = MicrosoftSTT(microsoft_stt_args)

    filename = "./tests/hello_world.wav"
    language = "en-GB"

    result = microsoft_stt.transcribe(filename, language)
    assert "hello world" in result.lower()
