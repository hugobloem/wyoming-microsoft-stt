import argparse  # noqa: D100
import asyncio
import logging
from functools import partial
import contextlib
import os  # Import to access environment variables
import signal
import re

from wyoming.info import AsrModel, AsrProgram, Attribution, Info
from wyoming.server import AsyncServer

from .download import get_languages
from .microsoft_stt import MicrosoftSTT
from .handler import MicrosoftEventHandler
from .version import __version__
from . import SpeechConfig

_LOGGER = logging.getLogger(__name__)

stop_event = asyncio.Event()


def handle_stop_signal(*args):
    """Handle shutdown signal and set the stop event."""
    _LOGGER.info("Received stop signal. Shutting down...")
    stop_event.set()


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--service-region",
        default=os.getenv("AZURE_SERVICE_REGION"),
        help="Microsoft Azure region (e.g., westus2)",
    )
    parser.add_argument(
        "--subscription-key",
        default=os.getenv("AZURE_SUBSCRIPTION_KEY"),
        help="Microsoft Azure subscription key",
    )
    parser.add_argument(
        "--uri", default="tcp://0.0.0.0:10300", help="unix:// or tcp://"
    )
    parser.add_argument(
        "--download-dir",
        default="/tmp/",
        help="Directory to download languages.json into (default: /tmp/)",
    )
    parser.add_argument(
        "--language",
        nargs="+",
        default=["en-GB"],
        help="List of languages to set for transcription (e.g., en-US fr-FR es-ES)",
    )
    parser.add_argument(
        "--update-languages",
        action="store_true",
        help="Download latest languages.json during startup",
    )
    parser.add_argument(
        "--profanity",
        default="masked",
        choices=["masked", "removed", "off"],
        help="Profanity setting for speech recognition",
    )
    parser.add_argument("--debug", action="store_true", help="Log DEBUG messages")
    return parser.parse_args()


def validate_args(args):
    """Validate command-line arguments."""
    if not args.service_region or not args.subscription_key:
        raise ValueError(
            "Both --service-region and --subscription-key must be provided either as command-line arguments or environment variables."
        )
    # Reinstate key validation with more flexibility to accommodate complex keys
    if not re.match(r"^[A-Za-z0-9\-_]{40,}$", args.subscription_key):
        _LOGGER.warning(
            "The subscription key does not match the expected format but will attempt to initialize."
        )


async def main() -> None:
    """Start Wyoming Microsoft STT server."""
    args = parse_arguments()
    validate_args(args)

    speech_config = SpeechConfig(
        subscription_key=args.subscription_key,
        service_region=args.service_region,
        profanity=args.profanity,
        language=args.language,
    )

    # Set up logging
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)
    _LOGGER.debug("Arguments parsed successfully.")

    # Load languages
    try:
        _LOGGER.info("Starting language loading process.")
        languages = get_languages(
            args.download_dir,
            update_languages=args.update_languages,
            region=args.service_region,
            key=args.subscription_key,
        )
        _LOGGER.info("Languages loaded successfully.")
    except Exception as e:
        _LOGGER.error(f"Failed to load languages: {e}")
        return

    wyoming_info = Info(
        asr=[
            AsrProgram(
                name="Microsoft",
                description="Microsoft speech transcription",
                attribution=Attribution(
                    name="Hugo Bloem",
                    url="https://github.com/hugobloem/wyoming-microsoft-stt/",
                ),
                version=__version__,
                installed=True,
                models=[
                    AsrModel(
                        name="Microsoft STT",
                        description="Microsoft speech transcription",
                        attribution=Attribution(
                            name="Hugo Bloem",
                            url="https://github.com/hugobloem/wyoming-microsoft-stt/",
                        ),
                        version=__version__,
                        installed=True,
                        languages=languages,
                    )
                ],
            )
        ],
    )

    # Load Microsoft STT model
    try:
        _LOGGER.debug("Loading Microsoft STT")
        stt_model = MicrosoftSTT(speech_config)
        _LOGGER.info("Microsoft STT model loaded successfully.")
    except Exception as e:
        _LOGGER.error(f"Failed to load Microsoft STT model: {e}")
        return

    # Initialize server and run
    server = AsyncServer.from_uri(args.uri)
    _LOGGER.info("Ready")
    model_lock = asyncio.Lock()
    try:
        await server.run(
            partial(
                MicrosoftEventHandler,
                wyoming_info,
                args,
                stt_model,
                model_lock,
            )
        )
    except Exception as e:
        _LOGGER.error(f"An error occurred while running the server: {e}")


if __name__ == "__main__":
    # Set up signal handling for graceful shutdown
    signal.signal(signal.SIGTERM, handle_stop_signal)
    signal.signal(signal.SIGINT, handle_stop_signal)

    with contextlib.suppress(KeyboardInterrupt):
        asyncio.run(main())
