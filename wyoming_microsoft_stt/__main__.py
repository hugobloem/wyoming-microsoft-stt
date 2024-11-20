import argparse  # noqa: D100
import asyncio
import logging
from functools import partial
import contextlib
import os  # Import to access environment variables

from wyoming.info import AsrModel, AsrProgram, Attribution, Info
from wyoming.server import AsyncServer

from .download import get_languages
from .microsoft_stt import MicrosoftSTT
from .handler import MicrosoftEventHandler
from .version import __version__

_LOGGER = logging.getLogger(__name__)

async def main() -> None:
    """Start Wyoming Microsoft STT server."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--service-region",
        default=os.getenv("AZURE_SERVICE_REGION"),  # Use environment variable as fallback
        help="Microsoft Azure region (e.g., westus2)",
    )
    parser.add_argument(
        "--subscription-key",
        default=os.getenv("AZURE_SUBSCRIPTION_KEY"),  # Use environment variable as fallback
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
        default="en-GB",
        help="Default language to set for transcription",
    )
    parser.add_argument(
        "--update-languages",
        action="store_true",
        help="Download latest languages.json during startup",
    )
    parser.add_argument("--debug", action="store_true", help="Log DEBUG messages")
    args = parser.parse_args()

    # Validate required arguments
    if not args.service_region or not args.subscription_key:
        raise ValueError("Both --service-region and --subscription-key must be provided either as command-line arguments or environment variables.")

    # Load languages
    languages = get_languages(
        args.download_dir,
        update_languages=args.update_languages,
        region=args.service_region,
        key=args.subscription_key,
    )

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)
    _LOGGER.debug(args)

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
    _LOGGER.debug("Loading Microsoft STT")
    stt_model = MicrosoftSTT(args)

    # Initialize server and run
    server = AsyncServer.from_uri(args.uri)
    _LOGGER.info("Ready")
    model_lock = asyncio.Lock()
    await server.run(
        partial(
            MicrosoftEventHandler,
            wyoming_info,
            args,
            stt_model,
            model_lock,
        )
    )

# -----------------------------------------------------------------------------

if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt):
        asyncio.run(main())
