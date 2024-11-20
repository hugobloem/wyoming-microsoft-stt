import azure.cognitiveservices.speech as speechsdk  # noqa: D100
import logging
import re

_LOGGER = logging.getLogger(__name__)


class MicrosoftSTT:
    """Class to handle Microsoft STT."""

    def __init__(self, args) -> None:
        """Initialize."""
        self.args = args
        try:
            # Simplify validation logic to focus on correct initialization
            if not args.subscription_key:
                _LOGGER.warning("No subscription key provided.")
            else:
                _LOGGER.debug(f"Using subscription key: {args.subscription_key}")

            self.speech_config = speechsdk.SpeechConfig(
                subscription=args.subscription_key, region=args.service_region
            )
            _LOGGER.info("Microsoft SpeechConfig initialized successfully.")
        except Exception as e:
            _LOGGER.error(f"Failed to initialize Microsoft SpeechConfig: {e}")
            raise

    def transcribe(self, filename: str, language=None):
        """Transcribe a file."""
        if language is None:
            language = self.args.language

        try:
            audio_config = speechsdk.audio.AudioConfig(filename=filename)
            # Creates a speech recognizer using a file as audio input, also specify the speech language
            speech_recognizer = speechsdk.SpeechRecognizer(
                speech_config=self.speech_config,
                language=language,
                audio_config=audio_config,
            )

            result = speech_recognizer.recognize_once()

            # Check the result
            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                _LOGGER.debug(f"Recognized: {result.text}")
                return result.text
            elif result.reason == speechsdk.ResultReason.NoMatch:
                _LOGGER.warning("No speech could be recognized.")
                return ""
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = result.cancellation_details
                _LOGGER.warning(f"Speech Recognition canceled: {cancellation_details.reason}")
                if cancellation_details.reason == speechsdk.CancellationReason.Error:
                    _LOGGER.error(f"Error details: {cancellation_details.error_details}")
                return ""
        except Exception as e:
            _LOGGER.error(f"Failed to transcribe audio file {filename}: {e}")
            return ""
