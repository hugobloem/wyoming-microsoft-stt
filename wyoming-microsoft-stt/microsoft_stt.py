import azure.cognitiveservices.speech as speechsdk
from pathlib import Path
import time
import logging
import tempfile

_LOGGER = logging.getLogger(__name__)

class MicrosoftSTT:
    def __init__(self, args) -> None:
        self.args = args
        self.speech_config = speechsdk.SpeechConfig(subscription=args.subscription_key, region=args.service_region)

        input_dir = str(tempfile.TemporaryDirectory())
        input_dir = Path(input_dir)
        input_dir.mkdir(parents=True, exist_ok=True)
        self.input_dir = input_dir

    def transcribe(self, filename, language=None):
        if language is None:
            language = self.args.language

        audio_config = speechsdk.audio.AudioConfig(filename=filename)
        # Creates a speech recognizer using a file as audio input, also specify the speech language
        speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=self.speech_config, language=language, audio_config=audio_config)
        
        result = speech_recognizer.recognize_once()

         # Check the result
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            _LOGGER.debug("Recognized: {}".format(result.text))
            return result.text
        elif result.reason == speechsdk.ResultReason.NoMatch:
            _LOGGER.warning("No speech could be recognized: {}".format(result.no_match_details))
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            _LOGGER.warning("Speech Recognition canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                _LOGGER.warning("Error details: {}".format(cancellation_details.error_details))