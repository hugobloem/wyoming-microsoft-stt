import azure.cognitiveservices.speech as speechsdk # noqa: D100
import logging

_LOGGER = logging.getLogger(__name__)

class MicrosoftSTT:
    """Class to handle Microsoft STT."""

    def __init__(self, args) -> None:
        """Initialize."""
        self.args = args
        self.speech_config = speechsdk.SpeechConfig(subscription=args.subscription_key, region=args.service_region)

    def transcribe(self, filename: str, language=None):
        """Transcribe a file."""
        if language is None:
            language = self.args.language

        audio_config = speechsdk.audio.AudioConfig(filename=filename)
        # Creates a speech recognizer using a file as audio input, also specify the speech language
        speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=self.speech_config, language=language, audio_config=audio_config)

        result = speech_recognizer.recognize_once()

        # Check the result
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            _LOGGER.debug(f"Recognized: {result.text}")
            return result.text
        elif result.reason == speechsdk.ResultReason.NoMatch:
            _LOGGER.warning(f"No speech could be recognized: {result.no_match_details}")
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            _LOGGER.warning(f"Speech Recognition canceled: {cancellation_details.reason}")
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                _LOGGER.warning(f"Error details: {cancellation_details.error_details}")
