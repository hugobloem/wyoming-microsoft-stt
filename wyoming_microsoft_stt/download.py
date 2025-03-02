"""Utility for downloading Microsoft STT languages."""

import logging
from pathlib import Path
from typing import Any, Union
from urllib.parse import quote, urlsplit, urlunsplit
from urllib.request import urlopen, Request
import json
import time
from urllib.error import URLError

URL_FORMAT = "https://{region}.cognitiveservices.azure.com/speechtotext/v3.1/transcriptions/locales"
URL_HEADER = "Ocp-Apim-Subscription-Key"

_DIR = Path(__file__).parent
_LOGGER = logging.getLogger(__name__)


def _quote_url(url: str) -> str:
    """Quote file part of URL in case it contains UTF-8 characters."""
    parts = list(urlsplit(url))
    parts[2] = quote(parts[2])
    return urlunsplit(parts)


def transform_languages_files(response):
    """Transform the languages.json file from the Microsoft API to the format used by Piper."""
    languages = json.load(response)
    return languages


def get_languages(
    download_dir: Union[str, Path],
    update_languages: bool = False,
    region: str = "westus",
    key: str = "",
) -> dict[str, Any]:
    """Load available languages from downloaded or embedded JSON file."""
    download_dir = Path(download_dir)
    if not download_dir.exists():
        download_dir.mkdir(parents=True)
    languages_download = download_dir.joinpath("languages.json")

    if update_languages:
        # Download latest languages.json with retry mechanism
        MAX_RETRIES = 3
        RETRY_DELAY = 5  # seconds
        for attempt in range(MAX_RETRIES):
            try:
                languages_url = URL_FORMAT.format(region=region)
                languages_hdr = {URL_HEADER: key}
                _LOGGER.debug("Downloading %s to %s", languages_url, languages_download)
                req = Request(_quote_url(languages_url), headers=languages_hdr)
                with urlopen(req) as response, open(
                    languages_download, "w"
                ) as download_file:
                    json.dump(
                        transform_languages_files(response), download_file, indent=4
                    )
                _LOGGER.info("Languages downloaded successfully.")
                break
            except URLError as e:
                _LOGGER.warning(
                    "Failed to download languages.json (attempt %d/%d): %s",
                    attempt + 1,
                    MAX_RETRIES,
                    e,
                )
                time.sleep(RETRY_DELAY)
            except Exception as e:
                _LOGGER.exception("Failed to download languages.json: %s", e)
                _LOGGER.error("Failed to update languages list")
                return {}

    # Prefer downloaded file to embedded
    if languages_download.exists():
        try:
            _LOGGER.debug("Loading %s", languages_download)
            with open(languages_download, encoding="utf-8") as languages_file:
                return json.load(languages_file)
        except Exception:
            _LOGGER.exception("Failed to load %s", languages_download)

    # Fall back to embedded
    languages_embedded = _DIR / "languages.json"
    try:
        _LOGGER.debug("Loading %s", languages_embedded)
        with open(languages_embedded, encoding="utf-8") as languages_file:
            return json.load(languages_file)
    except Exception:
        _LOGGER.exception("Failed to load embedded languages.json")
        return {}
