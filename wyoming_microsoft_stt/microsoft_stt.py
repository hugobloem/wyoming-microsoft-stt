"""Microsoft STT module for Wyoming."""

import threading
from typing import Optional
import azure.cognitiveservices.speech as speechsdk  # noqa: D100
import logging
from . import SpeechConfig

_LOGGER = logging.getLogger(__name__)


class MicrosoftSTT:
    """Class to handle Microsoft STT."""

    def __init__(self, speechconfig: SpeechConfig) -> None:
        """Initialize."""
        self.args = speechconfig

        self._stream = Optional[speechsdk.audio.PushAudioInputStream]
        self._speech_recognizer: Optional[speechsdk.SpeechRecognizer]
        self._results: list[speechsdk.SpeechRecognitionResult] = []

        try:
            # Initialize the speech configuration with the provided subscription key and region
            self.speech_config = speechsdk.SpeechConfig(
                subscription=self.args.subscription_key, region=self.args.service_region
            )
            _LOGGER.info("Microsoft SpeechConfig initialized successfully.")
        except Exception as e:
            _LOGGER.error(f"Failed to initialize Microsoft SpeechConfig: {e}")
            raise

        self.set_profanity(self.args.profanity)

    def start_transcribe(
        self,
        samples_per_second: int = 16000,
        bits_per_sample: int = 16,
        channels: int = 1,
        language=None,
    ) -> None:
        """Begin a transcription."""
        # Use the default language from args if no language is provided
        if language is None:
            language = self.args.language
        _LOGGER.debug(f"Starting transcription with language: {language}")

        # Configure audio input for speech recognition
        _LOGGER.debug("Configuring audio input stream...")
        self._stream = speechsdk.audio.PushAudioInputStream(
            stream_format=speechsdk.audio.AudioStreamFormat(
                samples_per_second=samples_per_second,
                bits_per_sample=bits_per_sample,
                channels=channels,
            )
        )
        audio_config = speechsdk.audio.AudioConfig(stream=self._stream)
        # Create a speech recognizer with the configured speech and audio settings
        self._speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=self.speech_config,
            language=language,
            audio_config=audio_config,
        )
        self.recognition_done = threading.Event()

        self._results = []

        def session_stopped_cb(evt):
            """Signal to stop continuous recognition upon receiving an event `evt`."""
            _LOGGER.debug(f"SESSION STOPPED: {evt}")
            self.recognition_done.set()

        self._speech_recognizer.recognizing.connect(
            lambda evt: _LOGGER.debug(f"RECOGNIZING: {evt}")
        )
        self._speech_recognizer.recognized.connect(
            lambda evt: _LOGGER.debug(f"RECOGNIZED: {evt}")
        )
        self._speech_recognizer.session_started.connect(
            lambda evt: _LOGGER.debug(f"SESSION STARTED: {evt}")
        )
        self._speech_recognizer.session_stopped.connect(session_stopped_cb)
        self._speech_recognizer.canceled.connect(
            lambda evt: _LOGGER.debug(f"CANCELED {evt}")
        )

        _LOGGER.debug("Starting continuous recognition...")

        def recognized(event: speechsdk.SpeechRecognitionEventArgs):
            _LOGGER.debug(f"{event.result}")
            self._results.append(event.result)

        self._speech_recognizer.start_continuous_recognition()
        self._speech_recognizer.recognized.connect(recognized)

    def push_audio_chunk(self, chunk: bytes):
        """Push an audio chunk to the recognizer."""
        self._stream.write(chunk)

    def transcribe(self):
        """Get the results of a transcription."""
        try:
            self._speech_recognizer.stop_continuous_recognition()

            return "\n".join(
                [
                    result.text
                    for result in self._results
                    if result.reason == speechsdk.ResultReason.RecognizedSpeech
                ]
            )

        except Exception as e:
            _LOGGER.error(f"Failed to transcribe audio: {e}")
            return ""

    def set_profanity(self, profanity: str):
        """Set the profanity filter level."""
        if profanity == "off":
            profanity_level = speechsdk.ProfanityOption.Raw
        elif profanity == "masked":
            profanity_level = speechsdk.ProfanityOption.Masked
        elif profanity == "removed":
            profanity_level = speechsdk.ProfanityOption.Removed
        else:
            _LOGGER.error(f"Invalid profanity level: {profanity}")
            return

        self.speech_config.set_profanity(profanity_level)
        _LOGGER.debug(f"Profanity filter set to {profanity}")
