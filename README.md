# MoMify - Private and local minutes of Meeting extraction

**Important Node : This app is only a proof of concept (PoC) to get hands on LangChain. It is far from "production-ready" state.**
It aims at extracting minutes of meetings (or MoM) from recorded videos of the desired meeting.
This application uses [OpenAI Whisper](https://github.com/openai/whisper) locally to extract the transcript fron the video, then asks a local LLM served by a local Ollama server to build a MoM from the transcript. Everything is made user-friendly using a Streamlit webapp.

## 1. Prerequisites

You have to options to run this app : use Docker to launch the containerized version of the app, or not.

If you want to use Docker, you'll need to have installed on the host machine :
- Docker - Podman in a near future
- [NVIDIA Container Toolkit⁠](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html#installation) if you want to take advantage of your Nvidia GPU in Ollama.

In case you don't want (or can) to use Docker, you need to have on your host :
- ffmpeg (required by Whiper)
- Poetry (dependencies manager)

### 1.1 Docker
Please refer to the [official documentation](https://docs.docker.com/engine/install/).

### 1.2 NVIDIA Container Toolkit⁠
If you want to use the container image of this projet with Nvidia GPU support you need to install [NVIDIA Container Toolkit⁠](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html#installation).

>> ⚠️ **Important note** :
>> If you don't use Docker to launch the app, you need to install other components. Please look at details below.

<details>

### 1.2 Poetry

This project is managed through Poetry 1.8.0.
Please refer to the [official documentation](https://python-poetry.org/docs/#installation).

### 1.3 ffmpeg

To install ffmpeg, use one of these :

```
# on Ubuntu or Debian
sudo apt update && sudo apt install ffmpeg

# on Arch Linux
sudo pacman -S ffmpeg

# on MacOS using Homebrew (https://brew.sh/)
brew install ffmpeg

# on Windows using Chocolatey (https://chocolatey.org/)
choco install ffmpeg

# on Windows using Scoop (https://scoop.sh/)
scoop install ffmpeg
```

</details>

## 2. Installation

At first run, you need to pull Ollama models once : 

```
docker-compose up -d
docker exec -it ollama ollama pull mistral
OR
docker exec -it ollama ollama pull llama3.2
```

If you  don't use Docker, you can run the followin to install the dependencies: `poetry install`

## 3. Run

If you want to use LangSmith (for debug purpose), you can add a .env file with : 

```
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
LANGCHAIN_API_KEY="Your-Api-Key"
LANGCHAIN_PROJECT="Your-Project-Name"
```

Then use : 
- this command if you don't want to use containers : `poetry run streamlit run ./MoMify/app.py`
- this one otherwise : `docker-compose up -d --build`

## Examples

The example is a simple translator and shows how to use LangChain + LangServe with Ollama.
You can run it through `poetry run python example.py` 

## Troubleshooting

### "FileNotFoundError: [WinError 2]"
You need to install `ffmpeg` on the host. See the prerequisites.