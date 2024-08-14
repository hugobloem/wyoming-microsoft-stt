"""Tests for the MicrosoftTTS class."""


def test_initialize(microsoft_stt):
    """Test initialization."""
    assert microsoft_stt.speech_config is not None


def test_transcribe(microsoft_stt):
    """Test synthesize."""
    filename = "./tests/hello_world.wav"
    language = "en-GB"

    result = microsoft_stt.transcribe(filename, language)
    assert "hello world" in result.lower()
