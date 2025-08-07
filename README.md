# Wyoming Microsoft STT
Wyoming protocol server for Microsoft Azure speech-to-text.

This Python package provides a Wyoming integration for Microsoft Azure speech-to-text and can be directly used with [Home Assistant](https://www.home-assistant.io/) voice and [Rhasspy](https://github.com/rhasspy/rhasspy3).

## Azure Speech Service
This program uses [Microsoft Azure Speech Service](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/). You can sign up to a free Azure account which comes with free tier of 5 audio hours per month, this should be enough for running a voice assistant as each command is relatively short. Once this amount is exceeded Azure could charge you for each second used (Current pricing is $0.36 per audio hour). I am not responsible for any incurred charges and recommend you set up a spending limit to reduce your exposure. However, for normal usage the free tier could suffice and the resource should not switch to a paid service automatically.

If you have not set up a speech resource, you can follow the instructions below. (you only need to do this once and works both for [Speech-to-Text](https://github.com/hugobloem/wyoming-microsoft-stt) and [Text-to-Speech](https://github.com/hugobloem/wyoming-microsoft-tts))

1. Sign in or create an account on [portal.azure.com](https://portal.azure.com).
2. Create a subscription by searching for `subscription` in the search bar. [Consult Microsoft Learn for more information](https://learn.microsoft.com/en-gb/azure/cost-management-billing/manage/create-subscription#create-a-subscription-in-the-azure-portal).
3. Create a speech resource by searching for `speech service`.
4. Select the subscription you created, pick or create a resource group, select a region, pick an identifiable name, and select the pricing tier (you probably want Free F0)
5. Once created, copy one of the keys from the speech service page. You will need this to run this program.

## Usage
Depending on the installation method parameters are parsed differently. However, the same options are used for each of the installation methods and can be found in the table below. Your service region and subscription key can be found on the speech service resource page (step 5 the Azure Speech service instructions).

For the bare-metal Python install the program is run as follows:
```python
python -m wyoming-microsoft-stt --<key> <value>
```

| Key | Optional | Description |
|---|---|---|
| `service-region` | No | Azure service region e.g., `uksouth` |
| `subscription-key` | No | Azure subscription key |
| `language` | Yes | Default language to set for transcription, default: `en-GB`. For auto-detection provide multiple languages. |
| `uri` | No | Uri where the server will be broadcasted e.g., `tcp://0.0.0.0:10300` |
| `download-dir` | Yes | Directory to download models into (default: ) |
| `update-languages` | Yes | Download latest languages.json during startup |
| `debug` | Yes | Log debug messages |

## Multi-language support
This add-on can also auto-detect the spoken language from a list of pre-defined languages (max. 10). To do this in Home Assistant provide the languages separated by semi-colons like so:
<img width="689" alt="Screenshot 2025-05-04 at 11 59 55" src="https://github.com/user-attachments/assets/b3c54fe5-ebf3-404a-a8e8-b0d27efaf76d" />

> [!NOTE]
> Setting multiple languages will override the options set by Home Assistant's Voice configuration! It will prompt you to select a language but the option is ignored when speech is processed.


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

  [![Open your Home Assistant instance and show the add add-on repository dialog with a specific repository URL pre-filled.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fhugobloem%2Fhomeassistant-addons)

- **Docker container**
  To run as a Docker container use the following command:
  ```bash
  docker run ghcr.io/hugobloem/wyoming-microsoft-stt-noha:latest --<key> <value>
  ```
  For the relevant keys please look at [the table below](#usage)

- **docker compose**

  Below is a sample for a docker compose file. The azure region + subscription key can be set in environment variables. Everything else needs to be passed via command line arguments.
  
  ```yaml
  wyoming-proxy-azure-stt:
    image: ghcr.io/hugobloem/wyoming-microsoft-stt-noha
    container_name: wyoming-azure-stt
    ports:
      - "10300:10300"
    environment:
      AZURE_SERVICE_REGION: swedencentral
      AZURE_SUBSCRIPTION_KEY: XXX
    command: --language=en-GB,nl-NL --uri=tcp://0.0.0.0:10300
  ```
