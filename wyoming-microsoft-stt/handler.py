"""Event handler for clients of the server."""
import argparse
import asyncio
import logging
import wave
import tempfile

from wyoming.asr import Transcribe, Transcript
from wyoming.audio import AudioChunk, AudioChunkConverter, AudioStop
from wyoming.event import Event
from wyoming.info import Describe, Info
from wyoming.server import AsyncEventHandler

from .microsoft_stt import MicrosoftSTT

_LOGGER = logging.getLogger(__name__)


class MicrosoftEventHandler(AsyncEventHandler):
    """Event handler for clients."""

    def __init__(
        self,
        wyoming_info: Info,
        cli_args: argparse.Namespace,
        model: MicrosoftSTT,
        model_lock: asyncio.Lock,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

        self.cli_args = cli_args
        self.wyoming_info_event = wyoming_info.event()
        self.model = model
        self.model_lock = model_lock
        self.audio = bytes()
        self.audio_converter = AudioChunkConverter(
            rate=16000,
            width=2,
            channels=1,
        )
        self._language = self.cli_args.language

        output_dir = str(tempfile.TemporaryDirectory() if not cli_args.debug else './tmp/')
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir = output_dir

    async def handle_event(self, event: Event) -> bool:
        if Describe.is_type(event.type):
            await self.write_event(self.wyoming_info_event)
            _LOGGER.debug("Sent info")
            return True

        if Transcribe.is_type(event.type):
            transcribe = Transcribe.from_event(event)
            if transcribe.language:
                self._language = transcribe.language
                _LOGGER.debug("Language set to %s", transcribe.language)
            return True

        if AudioChunk.is_type(event.type):
            if not self.audio:
                _LOGGER.debug("Receiving audio")

            chunk = AudioChunk.from_event(event)
            chunk = self.audio_converter.convert(chunk)
            self.audio += chunk.audio

            return True

        if AudioStop.is_type(event.type):
            _LOGGER.debug("Audio stopped")
            filename = self.output_dir / f"{time.monotonic_ns()}.wav"
            self.write_file(filename, self.audio)
            async with self.model_lock:
                text = self.model.transcribe(
                    filename,
                    language=self._language,
                )

            _LOGGER.info(text)

            await self.write_event(Transcript(text=text).event())
            _LOGGER.debug("Completed request")

            # Reset
            self.audio = bytes()
            self._language = self.cli_args.language

            return False

        return True

    def write_file(self, filename: str, data: bytes) -> None:
        """Write data to a  wav file."""
        wav_file: wave.Wave_write = wave.open(filename, "wb")
        with wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(16000)
            wav_file.writeframes(data)