# Langchain Transcript

## Prerequisites

This application uses [OpenAI Whisper](https://github.com/openai/whisper) locally.
It needs ffmpeg installed on the host : 

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

## Installation

This project is managed through Poetry 1.8.0.
You need to install it globally first (`pipx uninstall poetry`).
Then, you can run the followin to install the dependencies:

` poetry install `

This project relies on Ollama. 
In LangChain, the integration to use is the [ChatModel](https://python.langchain.com/docs/integrations/chat/ollama/), instead of older LLMs classes.
Run Ollama and get the model(s) : 

```
docker-compose up -d
docker exec -it ollama ollama pull mistral
docker exec -it ollama ollama pull llama3.2
```

## Run

Use this command
```
poetry run streamlit run app.py
```

## Examples

The example is a simple translator and shows how to use LangChain + LangServe with Ollama.
You can run it through `poetry run python example.py` 

## Troubleshooting

### "FileNotFoundError: [WinError 2]"
You need to install `ffmpeg` on the host. See the prerequisites.