# Langchain Transcript

## Installation

This project is managed through Poetry 1.8.0.
You need to install it globally first (`pipx uninstall poetry`).
Then, you can run the followin to install the dependencies:

` poetry install `

This project relies on Ollama. In LangChain, the integration to use is the [ChatModel](https://python.langchain.com/docs/integrations/chat/ollama/), instead of older LLMs classes.
Run Ollama and get the model(s) : 

```
docker-compose up -d
docker exec -it ollama ollama pull mistral
docker exec -it ollama ollama pull llama3.2
```

## Example

The example is a simple translator. You can serve it through `python example.py` 

## Run