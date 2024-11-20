"""Event handler for clients of the server."""
import argparse
import asyncio
import logging
import wave
import tempfile
from pathlib import Path
import time

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
        """Initialize."""
        super().__init__(*args, **kwargs)

        self.cli_args = cli_args
        self.wyoming_info_event = wyoming_info.event()
        self.model = model
        self.model_lock = model_lock
        self.audio = b""
        self.audio_converter = AudioChunkConverter(
            rate=16000,
            width=2,
            channels=1,
        )
        self._language = self.cli_args.language

        # Use /tmp for storing temporary files
        if not cli_args.debug:
            self._temp_dir = tempfile.TemporaryDirectory()
            output_dir = self._temp_dir.name
        else:
            output_dir = "/tmp/"

        # Set output_dir without explicitly creating it
        self.output_dir = Path(output_dir)

    async def handle_event(self, event: Event) -> bool:
        """Handle an event."""
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

            try:
                chunk = AudioChunk.from_event(event)
                chunk = self.audio_converter.convert(chunk)
                self.audio += chunk.audio
            except Exception as e:
                _LOGGER.error(f"Failed to convert audio chunk: {e}")
                return True

            return True

        if AudioStop.is_type(event.type):
            _LOGGER.debug("Audio stopped")
            filename = self.output_dir / f"{time.monotonic_ns()}.wav"
            try:
                self.write_file(str(filename), self.audio)
            except Exception as e:
                _LOGGER.error(f"Failed to write audio to file {filename}: {e}")
                return True

            async with self.model_lock:
                try:
                    start_time = time.time()
                    _LOGGER.debug("Starting transcription")
                    text = self.model.transcribe(
                        str(filename),
                        language=self._language,
                    )
                    _LOGGER.info(f"Transcription completed in {time.time() - start_time:.2f} seconds")
                except Exception as e:
                    _LOGGER.error(f"Failed to transcribe audio: {e}")
                    return True

            _LOGGER.info(text)

            await self.write_event(Transcript(text=text).event())
            _LOGGER.debug("Completed request")

            # Reset
            self.audio = b""
            self._language = self.cli_args.language

            # Clean up temporary file
            try:
                Path(filename).unlink()
                _LOGGER.debug(f"Deleted temporary audio file {filename}")
            except Exception as e:
                _LOGGER.warning(f"Failed to delete temporary audio file {filename}: {e}")

            return False

        return True

    def write_file(self, filename: str, data: bytes) -> None:
        """Write data to a wav file."""
        try:
            wav_file: wave.Wave_write = wave.open(filename, "wb")
            with wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(16000)
                wav_file.writeframes(data)
            _LOGGER.debug(f"Audio written to file {filename}")
        except Exception as e:
            _LOGGER.error(f"Failed to write wav file {filename}: {e}")
