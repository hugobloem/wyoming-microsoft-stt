import azure.cognitiveservices.speech as speechsdk  # noqa: D100
import logging
from . import SpeechConfig

_LOGGER = logging.getLogger(__name__)


class MicrosoftSTT:
    """Class to handle Microsoft STT."""

    def __init__(self, speechconfig: SpeechConfig) -> None:
        """Initialize."""
        self.args = speechconfig

        try:
            # Initialize the speech configuration with the provided subscription key and region
            self.speech_config = speechsdk.SpeechConfig(
                subscription=self.args.subscription_key, region=self.args.service_region
            )
            _LOGGER.info("Microsoft SpeechConfig initialized successfully.")
        except Exception as e:
            _LOGGER.error(f"Failed to initialize Microsoft SpeechConfig: {e}")
            raise

    def transcribe(self, filename: str, language=None):
        """Transcribe a file."""
        # Use the default language from args if no language is provided
        if language is None:
            language = self.args.language

        try:
            # Configure audio input for speech recognition
            audio_config = speechsdk.audio.AudioConfig(filename=filename)
            # Create a speech recognizer with the configured speech and audio settings
            speech_recognizer = speechsdk.SpeechRecognizer(
                speech_config=self.speech_config,
                language=language,
                audio_config=audio_config,
            )

            # Perform recognition on the audio file
            result = speech_recognizer.recognize_once()

            # Check the result and return the recognized text or log appropriate warnings
            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                _LOGGER.debug(f"Recognized: {result.text}")
                return result.text
            elif result.reason == speechsdk.ResultReason.NoMatch:
                _LOGGER.warning("No speech could be recognized.")
                return ""
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = result.cancellation_details
                _LOGGER.warning(
                    f"Speech Recognition canceled: {cancellation_details.reason}"
                )
                if cancellation_details.reason == speechsdk.CancellationReason.Error:
                    _LOGGER.error(
                        f"Error details: {cancellation_details.error_details}"
                    )
                return ""
        except Exception as e:
            _LOGGER.error(f"Failed to transcribe audio file {filename}: {e}")
            return ""
