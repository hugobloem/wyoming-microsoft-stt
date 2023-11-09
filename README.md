# Wyoming Microsoft STT
Wyoming protocol server for Microsoft Azure speech-to-text.

This Python package provides a Wyoming integration for Microsoft Azure speech-to-text and can be directly used with [Home Assistant](https://www.home-assistant.io/) voice and [Rhasspy](https://github.com/rhasspy/rhasspy3).

## Installation
Depending on your use case there are different installation options.

- **Using pip**
  Clone the repository and install the package using pip. Please note the platform requirements as noted [here](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/quickstarts/setup-platform?tabs=linux%2Cubuntu%2Cdotnetcli%2Cdotnet%2Cjre%2Cmaven%2Cnodejs%2Cmac%2Cpypi&pivots=programming-language-python#platform-requirements).
  ```sh
  pip install .
  ```

- **Home Assistant Add-On**
  Add the following repository as an add-on repository to your Home Assistant, or click the button below.
  [https://github.com/hugobloem/homeassistant-addons](https://github.com/hugobloem/homeassistant-addons)

  [![Open your Home Assistant instance and show the add add-on repository dialog with a specific repository URL pre-filled.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fhome-assistant%2Faddons-example)

- **Docker container**
  Coming soon...

## Usage
The same keys are used for each of the install methods. The service region and subscription key can be found in your [Azure portal](https://portal.azure.com).

| Key | Optional | Description |
|---|---|---|
| `service-region` | No | Azure service region e.g., `uksouth` |
| `subscription-key` | No | Azure subscription key |
| `uri` | No | Uri where the server will be broadcasted e.g., `tcp://0.0.0.0:10300` |
| `download-dir` | Yes | Directory to download models into (default: ) |
| `language` | Yes | Default language to set for transcription, default: `en-GB` |
| `update-languages` | Yes | Download latest languages.json during startup |
| `debug` | Yes | Log debug messages |