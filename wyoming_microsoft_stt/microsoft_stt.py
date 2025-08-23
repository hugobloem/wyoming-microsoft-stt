"""Microsoft STT module for Wyoming."""

import time
import azure.cognitiveservices.speech as speechsdk  # noqa: D100
import logging
from . import SpeechConfig

_LOGGER = logging.getLogger(__name__)


class MicrosoftSTT:
    """Class to handle Microsoft STT."""

    def __init__(self, speechconfig: SpeechConfig) -> None:
        """Initialize."""
        self.args = speechconfig

        self._stream: speechsdk.audio.PushAudioInputStream | None = None
        self._speech_recognizer: speechsdk.SpeechRecognizer | None = None
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
            audio_config=audio_config,
            **self.get_language(language),
        )

        self.recognition_done = False

        def session_stopped_cb(evt):
            """Signal to stop continuous recognition upon receiving an event `evt`."""
            _LOGGER.debug(f"SESSION STOPPED: {evt}")
            self.recognition_done = True

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
            self._results = event.result

        self._speech_recognizer.start_continuous_recognition()
        self._speech_recognizer.recognized.connect(recognized)

    def push_audio_chunk(self, chunk: bytes) -> None:
        """Push an audio chunk to the recognizer."""
        self._stream.write(chunk)

    def stop_audio_chunk(self) -> None:
        """Stop the transcription."""
        _LOGGER.debug("Stopping transcription...")
        self._stream.close()

    def transcribe(self):
        """Get the results of a transcription."""
        try:
            self.stop_audio_chunk()

            # Wait for the recognition to finish
            while not self.recognition_done:
                time.sleep(0.01)

            self._speech_recognizer.stop_continuous_recognition()

            return self._results.text

        except Exception as e:
            _LOGGER.error(f"Failed to transcribe audio: {e}")
            return ""

    def get_language(self, language: str) -> dict:
        """Get the language code."""
        if len(self.args.language) > 1:
            auto_detect_source_language_config = (
                speechsdk.languageconfig.AutoDetectSourceLanguageConfig(
                    languages=self.args.language
                )
            )
            return {
                "auto_detect_source_language_config": auto_detect_source_language_config
            }

        if language:
            _LOGGER.debug(f"Language set to {language}")
            return {"language": language}

        return {"language": self.args.language[0]}

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
